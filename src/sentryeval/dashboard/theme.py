"""Shared visual language for the Streamlit dashboard."""

from __future__ import annotations

from datetime import datetime

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap');

html, body, [class*="stApp"], .stMarkdown, .stCaption, p, label, input, textarea {
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif;
  color: #1c1917;
}
.stApp {
  background:
    radial-gradient(900px 320px at 8% -8%, #f8efe4 0%, transparent 58%),
    #f4f1ea;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"], footer,
[data-testid="stStatusWidget"], #MainMenu { visibility: hidden; height: 0; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] {
  background: #efeae2;
  border-right: 1px solid #ddd4c7;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #5c564e; }
.block-container { padding-top: 1.15rem; padding-bottom: 3rem; max-width: 1240px; }
h1, h2, h3 {
  font-family: "IBM Plex Serif", Georgia, serif;
  letter-spacing: -0.03em;
  font-weight: 600;
}
.brand {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin: 0.2rem 0 1.1rem 0;
  font-family: "IBM Plex Serif", Georgia, serif;
  font-size: 1.25rem;
  letter-spacing: -0.03em;
}
.brand-mark { color: #9a3412; font-size: 0.95rem; }
.hero-kicker {
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #7c746a;
  margin-bottom: 0.15rem;
}
.hero-title {
  font-family: "IBM Plex Serif", Georgia, serif;
  font-size: 2.05rem !important;
  line-height: 1.12;
  margin: 0 0 0.3rem 0;
}
.hero-sub { color: #5c564e; margin: 0 0 1.1rem 0; font-size: 0.98rem; }
.chip {
  display: inline-block;
  border: 1px solid #ddd4c7;
  background: #fffaf3;
  border-radius: 999px;
  padding: 0.18rem 0.7rem;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
}
.chip-ok { color: #3f5d45; border-color: #c9d6c4; background: #eef4ea; }
.chip-warn { color: #9a3412; border-color: #e8c4b4; background: #f8ece6; }
div[data-testid="stMetric"] {
  background: #fffaf3;
  border: 1px solid #ddd4c7;
  border-radius: 14px;
  padding: 0.75rem 0.9rem 0.85rem 0.9rem;
  overflow: visible;
}
div[data-testid="stMetricLabel"] { color: #7c746a; }
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] p,
div[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"] {
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif !important;
  font-size: 1.55rem !important;
  font-weight: 600;
  letter-spacing: -0.03em;
  overflow: visible !important;
  text-overflow: clip !important;
  white-space: nowrap !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 0.15rem;
  border-bottom: 1px solid #ddd4c7;
  background: transparent;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
  font-weight: 500;
  padding: 0.55rem 0.85rem;
  color: #7c746a;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: #9a3412 !important;
}
div[data-testid="stExpander"] {
  background: #fffaf3;
  border: 1px solid #ddd4c7;
  border-radius: 12px;
}
.risk-dot {
  display: inline-block;
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  margin-right: 0.4rem;
  vertical-align: middle;
}
.msg {
  border-left: 3px solid #ddd4c7;
  padding: 0.55rem 0.75rem;
  margin: 0.4rem 0;
  background: #faf7f1;
  border-radius: 0 10px 10px 0;
}
.msg-user { border-left-color: #9a3412; }
.msg-assistant { border-left-color: #3f5d45; }
.msg-system { border-left-color: #7c746a; }
.msg .role {
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #7c746a;
}
.msg .body { white-space: pre-wrap; margin-top: 0.15rem; }
div[data-testid="stDownloadButton"] button {
  border: 1px solid #ddd4c7;
  background: #fffaf3;
  color: #1c1917;
  border-radius: 10px;
  font-weight: 500;
}
div[data-testid="stDownloadButton"] button:hover {
  border-color: #9a3412;
  color: #9a3412;
}
</style>
"""

INK = "#1c1917"
PAPER = "#f4f1ea"
RUST = "#9a3412"
SAGE = "#3f5d45"
MUTED = "#7c746a"
STRETCH = "stretch"

MIME = {
    ".json": "application/json",
    ".jsonl": "application/jsonl",
    ".md": "text/markdown",
    ".html": "text/html",
}


def apply():
    import streamlit as st

    st.markdown(CSS, unsafe_allow_html=True)


def run_label(run_id: str, data: dict) -> str:
    stamp = data.get("run_timestamp", "")
    short = run_id[:8]
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        return f"{short}  ·  {dt.strftime('%d %b %H:%M')}"
    except (TypeError, ValueError):
        return short


def reliability_chip(data: dict) -> str:
    ok = bool(data.get("reliability_gate_passed", True))
    klass = "chip chip-ok" if ok else "chip chip-warn"
    label = "κ reliable" if ok else "κ warning"
    return f'<span class="{klass}">{label}</span>'


def mean_asr(data: dict) -> float:
    rows = [e for e in data.get("entries", []) if e.get("metric", "asr") == "asr"]
    return sum(e["value"] for e in rows) / max(1, len(rows))


def primary_kappa(data: dict) -> float | None:
    rows = data.get("judge_agreements") or []
    if not rows:
        return None
    return min(r.get("kappa", 0) for r in rows)


def n_samples(data: dict) -> int:
    rows = [e for e in data.get("entries", []) if e.get("metric", "asr") == "asr"]
    return int(sum(e.get("n_samples") or 0 for e in rows))


def risk_color(level: str) -> str:
    return {
        "critical": "#7f1d1d",
        "high": "#9a3412",
        "medium": "#b45309",
        "low": "#3f5d45",
        "minimal": "#3f5d45",
    }.get(str(level).lower(), MUTED)
