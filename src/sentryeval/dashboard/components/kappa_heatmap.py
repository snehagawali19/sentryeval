from sentryeval.dashboard.theme import INK, PAPER, RUST, SAGE


def matrix(rows):
    return {(r["judge_a"], r["judge_b"]): r["kappa"] for r in rows}


def figure(rows):
    import plotly.graph_objects as go

    judges = sorted({r["judge_a"] for r in rows} | {r["judge_b"] for r in rows})
    z = []
    for a in judges:
        row = []
        for b in judges:
            if a == b:
                row.append(1.0)
            else:
                row.append(matrix(rows).get((a, b), matrix(rows).get((b, a), None)))
        z.append(row)
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=judges,
            y=judges,
            zmin=0,
            zmax=1,
            colorscale=[
                [0.0, RUST],
                [0.6, "#e8c4b4"],
                [1.0, SAGE],
            ],
            colorbar={"title": "κ", "thickness": 12},
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER,
        font={"color": INK, "family": "IBM Plex Sans, sans-serif"},
        height=380,
        margin={"l": 80, "r": 24, "t": 12, "b": 80},
    )
    return fig
