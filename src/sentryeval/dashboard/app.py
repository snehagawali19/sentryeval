import json
from pathlib import Path

import streamlit as st

from sentryeval.dashboard import theme

st.set_page_config(page_title="SentryEval", page_icon="▣", layout="wide")
theme.apply()

runs_dir = Path("runs")
paths = sorted(runs_dir.glob("*/leaderboard.json"), key=lambda p: p.stat().st_mtime, reverse=True)
if not paths:
    st.markdown('<p class="hero-kicker">SentryEval</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">No runs yet</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Run <code>sentryeval run configs/quick_smoke.yaml</code>, then refresh.</p>',
        unsafe_allow_html=True,
    )
    st.stop()

payloads = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in paths}
labels = {rid: theme.run_label(rid, data) for rid, data in payloads.items()}

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">▣</span>SentryEval</div>',
        unsafe_allow_html=True,
    )
    choice = st.selectbox(
        "Run",
        options=list(payloads),
        format_func=lambda rid: labels[rid],
    )
    data = payloads[choice]
    st.markdown(theme.reliability_chip(data), unsafe_allow_html=True)
    st.caption(choice)
    st.markdown("**Downloads**")
    run_path = runs_dir / choice
    for name in ("leaderboard.json", "report.md", "report.html", "graveyard.html", "transcripts.jsonl"):
        target = run_path / name
        if not target.exists():
            continue
        st.download_button(
            label=name,
            data=target.read_bytes(),
            file_name=name,
            mime=theme.MIME.get(target.suffix, "application/octet-stream"),
            key=f"dl-{choice}-{name}",
            width=theme.STRETCH,
        )

st.markdown('<p class="hero-kicker">SentryEval</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Evaluation results</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="hero-sub">Attack success with 95% Wilson intervals. Lower ASR is safer. '
    f"Run {choice[:8]}.</p>",
    unsafe_allow_html=True,
)

kappa = theme.primary_kappa(data)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mean ASR", f"{theme.mean_asr(data):.1%}")
m2.metric("Judge κ", "—" if kappa is None else f"{kappa:.2f}")
m3.metric("Attempts", f"{theme.n_samples(data)}")
m4.metric("Models", str(len({e["model"] for e in data.get("entries", [])})))

tabs = st.tabs(["Leaderboard", "Graveyard", "Judges", "Attacks", "Compare"])
with tabs[0]:
    from sentryeval.dashboard.views.leaderboard import render

    render(data)
with tabs[1]:
    from sentryeval.dashboard.views.model_graveyard import render

    render(data.get("graveyard", []))
with tabs[2]:
    from sentryeval.dashboard.views.judge_agreement import render

    render(data.get("judge_agreements", []))
with tabs[3]:
    from sentryeval.dashboard.views.attack_explorer import render

    render(data)
with tabs[4]:
    from sentryeval.dashboard.views.run_comparison import render

    render(data, runs_dir)
