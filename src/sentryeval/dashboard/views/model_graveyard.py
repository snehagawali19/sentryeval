import streamlit as st

from sentryeval.dashboard.components.transcript_viewer import render as render_transcript
from sentryeval.dashboard.theme import risk_color


def _classify_risk(asr: float) -> str:
    if asr >= 0.8:
        return "critical"
    if asr >= 0.6:
        return "high"
    if asr >= 0.4:
        return "medium"
    if asr >= 0.2:
        return "low"
    return "minimal"


def render(entries):
    if not entries:
        st.info("No graveyard entries yet. Enable generate_graveyard on a run.")
        return
    cols = st.columns(min(len(entries), 4))
    for i, entry in enumerate(entries):
        with cols[i % 4]:
            level = entry["overall_risk_level"]
            st.metric(
                label=entry["model_name"].split("/")[-1],
                value=f"#{entry.get('rank_among_tested', '?')}",
                delta=level.upper(),
                delta_color="off",
            )
            st.markdown(
                f'<span class="risk-dot" style="background:{risk_color(level)}"></span>'
                f'<span class="chip">{entry["total_tests"]} tests</span>',
                unsafe_allow_html=True,
            )
    st.write("")
    for entry in entries:
        level = entry["overall_risk_level"]
        with st.expander(
            f"{entry['model_name']}   ·   rank #{entry.get('rank_among_tested', '?')}   ·   "
            f"{level} risk",
            expanded=(entry.get("rank_among_tested") == 1),
        ):
            if entry.get("surface_summary"):
                st.markdown("**By surface**")
                for surface, stats in entry["surface_summary"].items():
                    asr = stats["asr"]
                    risk = _classify_risk(asr)
                    st.markdown(
                        f'<span class="risk-dot" style="background:{risk_color(risk)}"></span>'
                        f"**{surface.replace('_', ' ')}**  ·  {asr:.0%} ASR  ·  "
                        f"95% CI [{stats['wilson_lower']:.0%}–{stats['wilson_upper']:.0%}]",
                        unsafe_allow_html=True,
                    )
            if not entry.get("failure_modes"):
                st.caption("No failure modes above the 10% ASR threshold.")
                continue
            st.markdown("**Failure modes**")
            for failure in entry.get("failure_modes", []):
                with st.expander(failure["failure_headline"]):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Attack**  \n`{failure['attack_name']}`")
                        st.markdown(
                            f"**ASR**  \n{failure['attack_success_rate']:.0%} "
                            f"[{failure['wilson_lower']:.0%}–{failure['wilson_upper']:.0%}]"
                        )
                    with c2:
                        st.markdown(f"**Root cause**  \n{failure['root_cause']}")
                        st.markdown(f"**Mitigation**  \n{failure['mitigation']}")
                    for j, transcript in enumerate(failure.get("exemplar_transcripts", [])[:3]):
                        st.caption(f"Exemplar {j + 1}")
                        render_transcript(transcript)
