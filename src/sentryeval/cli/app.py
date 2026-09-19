from dotenv import load_dotenv
from typer import Typer

from .commands.compare import compare
from .commands.dashboard import dashboard
from .commands.graveyard import graveyard
from .commands.judge_agree import judge_agreement
from .commands.run import run

load_dotenv()

app = Typer(
    name="sentryeval",
    help="SentryEval — AI Adversarial Evaluation Platform",
    rich_markup_mode="rich",
)
app.command()(run)
app.command("dashboard")(dashboard)
app.command("judge-agreement")(judge_agreement)
app.command()(graveyard)
app.command()(compare)

if __name__ == "__main__":
    app()
