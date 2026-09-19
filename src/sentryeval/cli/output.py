from rich.console import Console
from rich.panel import Panel

console = Console()


def print_run_banner(config_path, seed: int) -> None:
    console.print(
        Panel.fit(
            f"[bold cyan]SentryEval[/bold cyan]\nConfig: {config_path}\nSeed: {seed}",
            border_style="cyan",
        )
    )


def print_complete(run_id: str, run_dir: str) -> None:
    console.print(f"\n[green]Run complete![/green] ID: {run_id}\nResults: {run_dir}")
