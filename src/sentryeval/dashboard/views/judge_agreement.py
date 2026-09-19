import pandas as pd
import streamlit as st

from sentryeval.dashboard.components.kappa_heatmap import figure as kappa_figure
from sentryeval.dashboard.theme import STRETCH


def render(rows):
    st.caption("κ below 0.6 marks metrics as unreliable.")
    if not rows:
        st.info("Need at least two judges to compute Cohen's κ.")
        return
    st.plotly_chart(kappa_figure(rows), width=STRETCH)
    table = pd.DataFrame(rows)
    if "kappa" in table.columns:
        table = table.rename(
            columns={
                "judge_a": "Judge A",
                "judge_b": "Judge B",
                "kappa": "κ",
                "percent_agreement": "Agree %",
                "n_compared": "n",
                "interpretation": "Reading",
                "acceptable": "Pass",
            }
        )
    st.dataframe(table, width=STRETCH, hide_index=True)
