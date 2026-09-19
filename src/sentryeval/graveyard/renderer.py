from html import escape

CSS = """
:root { --ink:#1c1917; --paper:#f4f1ea; --card:#fffaf3; --line:#ddd4c7; --muted:#7c746a; --rust:#9a3412; --sage:#3f5d45; }
* { box-sizing: border-box; }
body { margin:0; font:16px/1.55 "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif; color:var(--ink); background:var(--paper); }
.wrap { max-width:980px; margin:0 auto; padding:2.5rem 1.4rem 4rem; }
h1,h2,h3 { font-family:"IBM Plex Serif", Georgia, serif; letter-spacing:-0.03em; font-weight:600; }
.kicker { font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted); }
.lede { color:var(--muted); max-width:42rem; }
section { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1.25rem 1.4rem; margin:1.1rem 0; }
.chip { display:inline-block; border:1px solid var(--line); border-radius:999px; padding:0.15rem 0.65rem; font-size:0.78rem; }
pre { white-space:pre-wrap; background:#faf7f1; border:1px solid var(--line); border-radius:10px; padding:0.8rem 1rem; }
ul { padding-left:1.1rem; }
"""


def render_markdown(entries):
    lines = ["# Model Graveyard", ""]
    for e in entries:
        lines += [
            f"## {e.model_name} — {e.overall_risk_level.value.upper()} risk",
            f"Rank: {e.rank_among_tested}; tests: {e.total_tests}",
            "",
        ]
        if e.surface_summary:
            lines.append("### Risk by surface")
            for surface, stats in e.surface_summary.items():
                lines.append(
                    f"- **{surface}**: {stats['asr']:.0%} ASR "
                    f"(95% CI [{stats['wilson_lower']:.0%}–{stats['wilson_upper']:.0%}], "
                    f"n={int(stats['n'])})"
                )
            lines.append("")
        if not e.failure_modes:
            lines += ["No failure modes above the 10% ASR reporting threshold.", ""]
            continue
        for f in e.failure_modes:
            lines += [
                f"### {f.failure_headline}",
                f"{f.failure_description}",
                f"- Surface: `{f.surface.value}`",
                f"- Attack: `{f.attack_name}`",
                f"- ASR: {f.attack_success_rate:.0%} "
                f"(95% CI [{f.wilson_lower:.0%}–{f.wilson_upper:.0%}])",
                f"- Root cause: {f.root_cause}",
                f"- Mitigation: {f.mitigation}",
                "",
            ]
            for i, t in enumerate(f.exemplar_transcripts[:3], 1):
                lines += [
                    f"#### Exemplar {i}",
                    f"Response: {t.response_text}",
                    "",
                ]
    return "\n".join(lines)


def render_html(entries):
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<title>Model Graveyard</title>",
        "<link rel='preconnect' href='https://fonts.googleapis.com'>",
        "<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600&display=swap' rel='stylesheet'>",
        f"<style>{CSS}</style></head><body><div class='wrap'>",
        "<p class='kicker'>SentryEval</p>",
        "<h1>Model graveyard</h1>",
        "<p class='lede'>Where each model failed, with Wilson intervals, root causes, and exemplar transcripts.</p>",
    ]
    for e in entries:
        parts.append("<section>")
        parts.append(
            f"<h2>{escape(e.model_name)}</h2>"
            f"<p><span class='chip'>{escape(e.overall_risk_level.value)}</span> "
            f"rank #{e.rank_among_tested} · {e.total_tests} tests</p>"
        )
        if e.surface_summary:
            parts.append("<h3>By surface</h3><ul>")
            for surface, stats in e.surface_summary.items():
                parts.append(
                    f"<li><strong>{escape(surface)}</strong>: {stats['asr']:.0%} ASR "
                    f"(95% CI [{stats['wilson_lower']:.0%}–{stats['wilson_upper']:.0%}])</li>"
                )
            parts.append("</ul>")
        if not e.failure_modes:
            parts.append("<p>No failure modes above the 10% ASR reporting threshold.</p>")
        for f in e.failure_modes:
            parts.append(f"<h3>{escape(f.failure_headline)}</h3>")
            parts.append(f"<p>{escape(f.failure_description)}</p>")
            parts.append(f"<p><strong>Root cause.</strong> {escape(f.root_cause)}</p>")
            parts.append(f"<p><strong>Mitigation.</strong> {escape(f.mitigation)}</p>")
            for i, t in enumerate(f.exemplar_transcripts[:3], 1):
                parts.append(f"<h4>Exemplar {i}</h4><pre>{escape(t.response_text)}</pre>")
        parts.append("</section>")
    parts.append("</div></body></html>")
    return "".join(parts)
