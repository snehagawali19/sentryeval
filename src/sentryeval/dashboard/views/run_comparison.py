import json
from pathlib import Path

import pandas as pd
import streamlit as st

from sentryeval.dashboard import theme
from sentryeval.dashboard.theme import STRETCH


def mean_asr(data):
    return theme.mean_asr(data)


def render(current, runs_dir=Path("runs")):
    paths = sorted(
        runs_dir.glob("*/leaderboard.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    ids = [p.parent.name for p in paths]
    if len(ids) < 2:
        st.info("Need two completed runs to compare.")
        return
    payloads = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in paths}
    labels = {rid: theme.run_label(rid, payloads[rid]) for rid in ids}
    left, right = st.columns(2)
    with left:
        run_a = st.selectbox("Run A", ids, index=0, format_func=lambda r: labels[r], key="cmp_a")
    with right:
        run_b = st.selectbox(
            "Run B", ids, index=min(1, len(ids) - 1), format_func=lambda r: labels[r], key="cmp_b"
        )
    a, b = payloads[run_a], payloads[run_b]
    c1, c2, c3 = st.columns(3)
    c1.metric("A mean ASR", f"{mean_asr(a):.1%}")
    c2.metric("B mean ASR", f"{mean_asr(b):.1%}")
    c3.metric("Delta B − A", f"{mean_asr(b) - mean_asr(a):+.1%}")

    def entry_key(e):
        return (e["model"], e["surface"], e["attack"], e["judge"], e.get("metric", "asr"))

    index_b = {entry_key(e): e for e in b.get("entries", [])}
    rows = []
    for e in a.get("entries", []):
        other = index_b.get(entry_key(e))
        rows.append(
            {
                "Model": e["model"],
                "Surface": e["surface"].replace("_", " "),
                "Attack": e["attack"],
                "Judge": e["judge"],
                "Metric": e.get("metric", "asr"),
                "A": e["value"],
                "A CI": f"{e['wilson_lower']:.1%} – {e['wilson_upper']:.1%}",
                "B": other["value"] if other else None,
                "B CI": (
                    f"{other['wilson_lower']:.1%} – {other['wilson_upper']:.1%}" if other else "—"
                ),
                "Δ": (other["value"] - e["value"]) if other else None,
            }
        )
    st.dataframe(
        pd.DataFrame(rows),
        width=STRETCH,
        hide_index=True,
        column_config={
            "A": st.column_config.NumberColumn(format="%.1%"),
            "B": st.column_config.NumberColumn(format="%.1%"),
            "Δ": st.column_config.NumberColumn(format="%+.1%"),
        },
    )
