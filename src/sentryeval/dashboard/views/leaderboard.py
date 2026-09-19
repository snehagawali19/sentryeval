import pandas as pd
import streamlit as st

from sentryeval.dashboard.components.wilson_chart import figure as wilson_figure
from sentryeval.dashboard.theme import STRETCH


def render(data):
    entries = [e for e in data.get("entries", []) if e.get("metric", "asr") == "asr"]
    if not entries:
        st.info("No metric results to display.")
        return
    st.caption("Every ASR includes a 95% Wilson interval. Lower is safer.")
    left, mid, right = st.columns([1, 1, 1.2])
    surfaces = ["all", *sorted({e["surface"] for e in entries})]
    judges = sorted({e["judge"] for e in entries})
    with left:
        selected_surface = st.selectbox("Surface", surfaces, key="lb_surface")
    with mid:
        selected_judge = st.selectbox("Judge", judges, key="lb_judge") if judges else None
    with right:
        query = st.text_input("Search", placeholder="Model or attack…", key="lb_search")
    if selected_surface != "all":
        entries = [e for e in entries if e["surface"] == selected_surface]
    if selected_judge:
        entries = [e for e in entries if e["judge"] == selected_judge]
    if query:
        needle = query.lower()
        entries = [
            e
            for e in entries
            if needle in e["model"].lower()
            or needle in e["attack"].lower()
            or needle in e["surface"].lower()
        ]
    if not entries:
        st.info("No rows match those filters.")
        return
    st.plotly_chart(wilson_figure(entries), width=STRETCH)
    rows = [
        {
            "Model": e["model"],
            "Surface": e["surface"].replace("_", " "),
            "Attack": e["attack"],
            "ASR": e["value"],
            "CI": f"{e['wilson_lower']:.1%} – {e['wilson_upper']:.1%}",
            "n": e.get("n_samples", "—"),
            "κ": e.get("judge_kappa") if e.get("judge_kappa") is not None else "—",
            "Reliable": "yes" if e.get("reliable", True) else "low κ",
        }
        for e in entries
    ]
    st.dataframe(
        pd.DataFrame(rows),
        width=STRETCH,
        hide_index=True,
        column_config={
            "ASR": st.column_config.ProgressColumn("ASR", min_value=0, max_value=1, format="%.1%"),
        },
    )
