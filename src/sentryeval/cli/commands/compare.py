from pathlib import Path

import orjson
from rich.table import Table

from ..output import console


def _load(runs_dir: Path, run_id: str):
    return orjson.loads((runs_dir / run_id / "leaderboard.json").read_bytes())


def compare(
    run_id_a: str,
    run_id_b: str,
    runs_dir: Path = Path("runs"),
):
    """Compare two evaluation runs side by side."""
    a = _load(runs_dir, run_id_a)
    b = _load(runs_dir, run_id_b)
    console.print(f"[cyan]Comparing {run_id_a[:8]} vs {run_id_b[:8]}[/cyan]")
    def entry_key(e):
        return (e["model"], e["surface"], e["attack"], e["judge"], e["metric"])

    index_b = {entry_key(e): e for e in b.get("entries", [])}
    table = Table("Model", "Surface", "Attack", "Judge", "Metric", "A", "B", "Delta")
    for e in a.get("entries", []):
        other = index_b.get(entry_key(e))
        bv = other["value"] if other else None
        delta = (bv - e["value"]) if bv is not None else None
        table.add_row(
            e["model"],
            e["surface"],
            e["attack"],
            e["judge"],
            e["metric"],
            f"{e['value']:.1%} [{e['wilson_lower']:.1%}, {e['wilson_upper']:.1%}]",
            (
                f"{bv:.1%} [{other['wilson_lower']:.1%}, {other['wilson_upper']:.1%}]"
                if other
                else "—"
            ),
            f"{delta:+.1%}" if delta is not None else "—",
        )
    console.print(table)
