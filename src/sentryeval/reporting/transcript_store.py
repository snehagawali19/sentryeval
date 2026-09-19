from pathlib import Path

import orjson

from ..core.models import Attempt, TranscriptRecord


def transcript_records(attempts: list[Attempt], config_hash: str = "") -> list[TranscriptRecord]:
    rows = []
    for a in attempts:
        rows.append(
            TranscriptRecord(
                run_id=a.run_id,
                attempt_id=a.attempt_id,
                behavior_id=a.behavior_id,
                surface=a.surface.value,
                attack_name=a.attack_name,
                target_name=a.target_name,
                seed=a.seed,
                timestamp_utc=a.timestamp_utc,
                prompt_messages=a.prompt_messages,
                response_text=a.response_text,
                verdicts=dict(a.verdicts),
                scores=dict(a.scores),
                provenance={
                    "dataset_version": a.dataset_version,
                    "metric_name": "asr",
                    "config_hash": config_hash,
                },
                token_usage={
                    "prompt_tokens": a.prompt_tokens,
                    "completion_tokens": a.completion_tokens,
                },
                cost_usd=a.cost_usd,
            )
        )
    return rows


class TranscriptStore:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def replace(self, attempts: list[Attempt], config_hash: str = ""):
        with self.path.open("wb") as f:
            for row in transcript_records(attempts, config_hash):
                f.write(orjson.dumps(row.model_dump(mode="json")) + b"\n")

    def load_raw(self):
        if not self.path.exists():
            return []
        return [
            orjson.loads(line)
            for line in self.path.read_bytes().splitlines()
            if line
        ]
