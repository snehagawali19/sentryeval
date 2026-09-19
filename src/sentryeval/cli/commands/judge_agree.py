from pathlib import Path

import orjson
import typer

from ...core.models import Attempt, Message, ThreatSurface, Verdict
from ...statistics.cohen_kappa import cohen_kappa
from ..output import console


def _attempts_from_transcripts(path: Path) -> list[Attempt]:
    grouped: dict[str, Attempt] = {}
    for raw in path.read_bytes().splitlines():
        if not raw:
            continue
        row = orjson.loads(raw)
        aid = row["attempt_id"]
        if aid not in grouped:
            grouped[aid] = Attempt(
                attempt_id=aid,
                run_id=row["run_id"],
                behavior_id=row["behavior_id"],
                dataset_version=row.get("provenance", {}).get("dataset_version", ""),
                attack_name=row["attack_name"],
                target_name=row["target_name"],
                surface=ThreatSurface(row["surface"]),
                seed=row["seed"],
                prompt_messages=[Message.model_validate(m) for m in row.get("prompt_messages", [])],
                response_text=row["response_text"],
                timestamp_utc=row.get("timestamp_utc", ""),
                prompt_tokens=row.get("token_usage", {}).get("prompt_tokens", 0),
                completion_tokens=row.get("token_usage", {}).get("completion_tokens", 0),
                cost_usd=row.get("cost_usd", 0.0),
            )
        if row.get("verdicts"):
            for judge, verdict in row["verdicts"].items():
                grouped[aid].verdicts[judge] = Verdict(verdict)
                grouped[aid].scores[judge] = float((row.get("scores") or {}).get(judge, 0.0))
        elif row.get("judge_name"):
            judge = row["judge_name"]
            grouped[aid].verdicts[judge] = Verdict(row["verdict"])
            grouped[aid].scores[judge] = float(row.get("score", 0.0))
    return list(grouped.values())


def judge_agreement(
    run_id: str = typer.Argument(..., help="Run ID to analyze"),
    runs_dir: Path = Path("runs"),
):
    """Compute and display inter-judge agreement (Cohen's κ) for a completed run."""
    path = runs_dir / run_id / "transcripts.jsonl"
    attempts = _attempts_from_transcripts(path)
    judges = sorted({j for a in attempts for j in a.verdicts})
    if len(judges) < 2:
        console.print("[yellow]Need at least two judges on the transcripts.[/yellow]")
        return
    console.print(f"[cyan]Computing judge agreement for run {run_id}[/cyan]")
    for i, ja in enumerate(judges):
        for jb in judges[i + 1 :]:
            agreement = cohen_kappa(ja, jb, attempts)
            console.print(
                f"{agreement.judge_a} vs {agreement.judge_b}: "
                f"kappa={agreement.kappa:.3f} ({agreement.interpretation}, "
                f"n={agreement.n_compared})"
            )
