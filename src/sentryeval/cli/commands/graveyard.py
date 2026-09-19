from pathlib import Path

import orjson
import typer

from ...core.models import GraveyardEntry
from ...graveyard.renderer import render_html, render_markdown
from ..output import console


def graveyard(
    run_id: str = typer.Argument(..., help="Run ID"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output path for Markdown"),
    runs_dir: Path = Path("runs"),
):
    """Generate or display the model graveyard for a run."""
    run_path = runs_dir / run_id
    html_path = run_path / "graveyard.html"
    board = orjson.loads((run_path / "leaderboard.json").read_bytes())
    entries = [GraveyardEntry.model_validate(e) for e in board.get("graveyard", [])]
    md = render_markdown(entries)
    if output:
        output.write_text(md, encoding="utf-8")
        console.print(str(output.resolve()))
        return
    if not html_path.exists():
        html_path.write_text(render_html(entries), encoding="utf-8")
        (run_path / "graveyard.md").write_text(md, encoding="utf-8")
    console.print(f"[cyan]Building graveyard for run {run_id}[/cyan]")
    console.print(str(html_path.resolve()))
