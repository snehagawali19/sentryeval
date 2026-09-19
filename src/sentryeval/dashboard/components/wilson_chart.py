"""Plotly Wilson CI bar chart helpers."""

from sentryeval.dashboard.theme import INK, RUST


def interval(entry):
    return entry["value"], entry["wilson_lower"], entry["wilson_upper"]


def figure(entries):
    import plotly.graph_objects as go

    fig = go.Figure()
    models = sorted({e["model"] for e in entries})
    for model in models:
        model_entries = [e for e in entries if e["model"] == model]
        if not model_entries:
            continue
        avg_asr = sum(e["value"] for e in model_entries) / len(model_entries)
        avg_lower = sum(e["wilson_lower"] for e in model_entries) / len(model_entries)
        avg_upper = sum(e["wilson_upper"] for e in model_entries) / len(model_entries)
        fig.add_trace(
            go.Bar(
                name=model,
                x=[model.split("/")[-1]],
                y=[avg_asr],
                marker_color=INK,
                error_y={
                    "type": "data",
                    "symmetric": False,
                    "array": [avg_upper - avg_asr],
                    "arrayminus": [avg_asr - avg_lower],
                    "visible": True,
                    "color": RUST,
                    "thickness": 2,
                    "width": 8,
                },
                hovertemplate=(
                    f"<b>{model}</b><br>ASR: {avg_asr:.1%}<br>"
                    f"95% CI: [{avg_lower:.1%}, {avg_upper:.1%}]<extra></extra>"
                ),
            )
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": INK, "family": "IBM Plex Sans, sans-serif"},
        yaxis={
            "title": "Attack success rate",
            "tickformat": ".0%",
            "range": [0, 1],
            "gridcolor": "#ddd4c7",
            "zeroline": False,
        },
        xaxis={"title": "", "tickangle": 0},
        showlegend=False,
        height=360,
        margin={"l": 48, "r": 12, "t": 12, "b": 48},
        bargap=0.45,
    )
    return fig
