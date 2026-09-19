import pandas as pd
import streamlit as st

from sentryeval.dashboard.theme import STRETCH


def render(data):
    st.caption("Every attack and surface in this run, with Wilson bounds.")
    rows = [
        {
            "Surface": e["surface"].replace("_", " "),
            "Attack": e["attack"],
            "Dataset": e["dataset"],
            "Judge": e["judge"],
            "Metric": e["metric"],
            "n": e["n_samples"],
            "ASR": e["value"],
            "CI": f"{e['wilson_lower']:.1%} – {e['wilson_upper']:.1%}",
        }
        for e in data.get("entries", [])
    ]
    if not rows:
        st.info("No attacks in this run.")
        return
    surfaces = ["all", *sorted({r["Surface"] for r in rows})]
    selected = st.selectbox("Surface", surfaces, key="atk_surface")
    table = pd.DataFrame(rows).drop_duplicates()
    if selected != "all":
        table = table[table["Surface"] == selected]
    st.dataframe(
        table,
        width=STRETCH,
        hide_index=True,
        column_config={
            "ASR": st.column_config.ProgressColumn("Value", min_value=0, max_value=1, format="%.1%"),
        },
    )
