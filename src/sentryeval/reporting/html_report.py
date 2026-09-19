from html import escape

from .markdown_report import render as render_markdown

CSS = """
:root { --ink:#1c1917; --paper:#f4f1ea; --card:#fffaf3; --line:#ddd4c7; --muted:#7c746a; --rust:#9a3412; }
* { box-sizing: border-box; }
body { margin:0; font:15px/1.5 "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif; color:var(--ink); background:var(--paper); }
.wrap { max-width:1100px; margin:0 auto; padding:2.4rem 1.4rem 4rem; }
h1,h2 { font-family:"IBM Plex Serif", Georgia, serif; letter-spacing:-0.03em; }
.kicker { font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted); }
.lede { color:var(--muted); }
table { border-collapse:collapse; width:100%; background:#fffaf3; }
th,td { border-bottom:1px solid var(--line); padding:0.55rem 0.65rem; text-align:left; vertical-align:top; }
th { color:var(--muted); font-weight:500; font-size:0.8rem; letter-spacing:0.04em; }
.warn { color:var(--rust); }
pre { white-space:pre-wrap; background:#fffaf3; border:1px solid var(--line); border-radius:12px; padding:1rem; }
"""


def render(leaderboard):
    md = render_markdown(leaderboard)
    rows = []
    for e in leaderboard.get("entries", []):
        badge = "yes" if e.get("reliable", True) else "low κ"
        klass = "" if e.get("reliable", True) else "warn"
        rows.append(
            "<tr>"
            f"<td>{escape(str(e['model']))}</td>"
            f"<td>{escape(str(e['surface'])).replace('_', ' ')}</td>"
            f"<td>{escape(str(e['attack']))}</td>"
            f"<td>{escape(str(e['judge']))}</td>"
            f"<td>{escape(str(e['metric']))}</td>"
            f"<td>{e['value']:.1%} [{e['wilson_lower']:.1%}, {e['wilson_upper']:.1%}]</td>"
            f"<td>{e.get('n_samples', '—')}</td>"
            f"<td class='{klass}'>{escape(badge)}</td>"
            "</tr>"
        )
    table = (
        "<table><thead><tr>"
        "<th>Model</th><th>Surface</th><th>Attack</th><th>Judge</th>"
        "<th>Metric</th><th>Value (95% CI)</th><th>n</th><th>Reliable</th>"
        "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )
    gate = "pass" if leaderboard.get("reliability_gate_passed") else "warning"
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>SentryEval Report</title>"
        "<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600&display=swap' rel='stylesheet'>"
        f"<style>{CSS}</style></head><body><div class='wrap'>"
        "<p class='kicker'>SentryEval</p>"
        "<h1>Evaluation report</h1>"
        f"<p class='lede'>Run {escape(str(leaderboard.get('run_id', '')))} · reliability {gate}. "
        "Every ASR includes a 95% Wilson interval.</p>"
        f"{table}<h2>Source markdown</h2><pre>{escape(md)}</pre></div></body></html>"
    )
    return html
