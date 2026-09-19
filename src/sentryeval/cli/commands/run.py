import asyncio
from pathlib import Path

import typer

from ...runner.orchestrator import SentryEvalRunner
from ..output import console, print_complete, print_run_banner


def run(
    config: Path = typer.Argument(..., exists=True, help="Path to YAML config file"),
    seed: int | None = typer.Option(None, "--seed", help="Random seed for reproducibility"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate config without running"),
    allow_live: bool = typer.Option(False, "--allow-live", help="Permit live model and judge calls"),
):
    """Execute an evaluation run from a config file."""
    runner = SentryEvalRunner.from_config(config, allow_live=allow_live)
    if seed is not None:
        runner.seed = seed
        runner.config["seed"] = seed
    print_run_banner(config, runner.seed)
    if dry_run:
        console.print(f"[green]Valid config[/green]; live access={allow_live}")
        return
    result = asyncio.run(runner.run())
    print_complete(result["run_id"], result["run_dir"])
