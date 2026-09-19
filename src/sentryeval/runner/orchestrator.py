import random
import uuid
from pathlib import Path
from typing import Any

import numpy as np
import orjson
import yaml

from ..core.exceptions import ConfigurationError, LiveTargetDisabledError
from ..core.registry import get_attack, get_dataset, get_judge, get_target
from ..graveyard.builder import GraveyardBuilder
from ..graveyard.renderer import render_html as graveyard_html
from ..graveyard.renderer import render_markdown as graveyard_markdown
from ..provenance.tracker import config_hash
from ..reporting.html_report import render as html_report
from ..reporting.leaderboard import build_leaderboard
from ..reporting.markdown_report import render as markdown_report
from ..reporting.transcript_store import TranscriptStore
from ..statistics.aggregator import aggregate
from ..statistics.cohen_kappa import cohen_kappa
from .budget import BudgetTracker
from .cache import ResultCache


class SentryEvalRunner:
    def __init__(self, config: dict[str, Any], runs_dir=None, allow_live=False):
        self.config = config
        self.allow_live = allow_live
        self.seed = int(config.get("seed", 42))
        self.run_id = str(uuid.uuid4())
        self.config_hash = config_hash(config)
        out = config.get("output", {})
        self.output = out
        self.runs_dir = Path(runs_dir or out.get("runs_dir", "runs"))
        self.run_dir = self.runs_dir / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts = TranscriptStore(self.run_dir / "transcripts.jsonl")
        self.cache = ResultCache(Path(config.get("cache_dir", ".cache/sentryeval")))
        self.budget = BudgetTracker(config.get("max_queries", 1000), config.get("max_tokens"))
        random.seed(self.seed)
        np.random.seed(self.seed)

    @classmethod
    def from_config(cls, path, runs_dir=None, allow_live=False):
        with Path(path).open(encoding="utf-8") as f:
            config = yaml.safe_load(f)
        if not isinstance(config, dict):
            raise ConfigurationError("Config root must be a mapping")
        return cls(config, runs_dir, allow_live)

    def _items(self, key):
        return [({"name": x} if isinstance(x, str) else x) for x in self.config.get(key, [])]

    def _flag(self, name, default=True):
        return bool(self.output.get(name, default))

    async def run(self):
        targets = [
            get_target(x if isinstance(x, str) else x) for x in self.config.get("targets", [])
        ]
        attacks = [get_attack(x["name"], x.get("params")) for x in self._items("attacks")]
        datasets = [get_dataset(x["name"]) for x in self._items("datasets")]
        judges = [get_judge(x["name"], x.get("params")) for x in self._items("judges")]
        live = [x.name for x in [*targets, *judges] if getattr(x, "is_live", False)]
        if live and not self.allow_live:
            raise LiveTargetDisabledError(f"Live components require --allow-live: {live}")
        attempts = []
        behavior_index = {}
        for ds in datasets:
            behaviors = ds.load()
            for b in behaviors:
                behavior_index[b.behavior_id] = b
            for target in targets:
                for attack in attacks:
                    for b in behaviors:
                        key = self.cache.make_key(
                            attack.name,
                            target.name,
                            ds.sha256,
                            b.behavior_id,
                            self.seed,
                            attack_params=vars(attack),
                            target_params={"model_id": target.model_id},
                            hyperparameters={"temperature": 0},
                        )
                        rows = self.cache.get(key)
                        if rows is None:
                            rows = await attack.run(b, target, self.seed)
                            for a in rows:
                                a.run_id = self.run_id
                            self.cache.set(key, rows)
                            self.budget.consume(
                                len(rows), sum(a.prompt_tokens + a.completion_tokens for a in rows)
                            )
                        else:
                            for a in rows:
                                a.run_id = self.run_id
                                a.attempt_id = str(uuid.uuid4())
                        attempts.extend(rows)
        for judge in judges:
            for a in attempts:
                try:
                    verdict, score = await judge.score(behavior_index[a.behavior_id], a)
                except Exception:
                    from ..core.models import Verdict

                    verdict, score = Verdict.ERROR, 0
                a.verdicts[judge.judge_id] = verdict
                a.scores[judge.judge_id] = score
        if self._flag("save_transcripts", True):
            self.transcripts.replace(attempts, self.config_hash)
        threshold = float(self.config.get("judge_agreement", {}).get("require_kappa_above", 0.6))
        agreements = [
            cohen_kappa(judges[i].judge_id, judges[j].judge_id, attempts, threshold)
            for i in range(len(judges))
            for j in range(i + 1, len(judges))
        ]
        metric_names = self.config.get("metrics") or ["asr"]
        metrics = aggregate(
            attempts,
            judges,
            self.run_id,
            self.config_hash,
            agreements,
            threshold,
            metric_names=metric_names,
        )
        graveyard = GraveyardBuilder(self.run_id, self.config_hash).build(
            attempts, metrics, targets
        )
        leaderboard = build_leaderboard(
            self.run_id, self.config_hash, metrics, agreements, graveyard
        )
        html_flag = self._flag("generate_html_report", False)
        grave_flag = self._flag("generate_graveyard", False)
        if self._flag("save_leaderboard", True):
            (self.run_dir / "leaderboard.json").write_bytes(
                orjson.dumps(leaderboard, option=orjson.OPT_INDENT_2)
            )
            (self.run_dir / "report.md").write_text(markdown_report(leaderboard), encoding="utf-8")
        if html_flag:
            (self.run_dir / "report.html").write_text(html_report(leaderboard), encoding="utf-8")
        if grave_flag:
            (self.run_dir / "graveyard.html").write_text(graveyard_html(graveyard), encoding="utf-8")
            (self.run_dir / "graveyard.md").write_text(
                graveyard_markdown(graveyard), encoding="utf-8"
            )
        self.cache.close()
        return {
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "metric_results": metrics,
            "judge_agreements": agreements,
            "graveyard": graveyard,
            "leaderboard": leaderboard,
            "attempts": attempts,
        }
