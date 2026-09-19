import subprocess
import sys
from pathlib import Path

from ..output import console


def dashboard():
    """Launch the Streamlit dashboard."""
    app_path = Path(__file__).resolve().parents[2] / "dashboard" / "app.py"
    console.print("[cyan]Launching SentryEval dashboard...[/cyan]")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)
