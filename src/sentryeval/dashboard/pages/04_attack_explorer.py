import json
from pathlib import Path

from sentryeval.dashboard import theme
from sentryeval.dashboard.views.attack_explorer import render


def _standalone():
    import streamlit as st

    st.set_page_config(page_title="Attacks", layout="wide")
    theme.apply()
    paths = sorted(Path("runs").glob("*/leaderboard.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not paths:
        st.warning("No runs found.")
        return
    data = json.loads(paths[0].read_text(encoding="utf-8"))
    render(data)


_standalone()
