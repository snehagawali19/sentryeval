from pathlib import Path

from sentryeval.dashboard import theme
from sentryeval.dashboard.views.run_comparison import render


def _standalone():
    import streamlit as st

    st.set_page_config(page_title="Compare", layout="wide")
    theme.apply()
    if not list(Path("runs").glob("*/leaderboard.json")):
        st.warning("No runs found.")
        return
    render({}, Path("runs"))


_standalone()
