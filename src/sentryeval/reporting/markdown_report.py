def render(leaderboard):
    lines = [
        f"# SentryEval Report — {leaderboard['run_id']}",
        "",
        f"Reliability gate: **{'PASS' if leaderboard.get('reliability_gate_passed') else 'WARNING'}**",
        "",
        "Every ASR below includes a 95% Wilson confidence interval. "
        "Raw ASR is never reported alone.",
        "",
        "| Model | Surface | Attack | Judge | Metric | Value (95% CI) | n | Reliable |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for e in leaderboard.get("entries", []):
        badge = "yes" if e.get("reliable", True) else "WARNING low kappa"
        lines.append(
            f"| {e['model']} | {e['surface']} | {e['attack']} | {e['judge']} | {e['metric']} | "
            f"{e['value']:.1%} [{e['wilson_lower']:.1%}, {e['wilson_upper']:.1%}] | "
            f"{e.get('n_samples', '—')} | {badge} |"
        )
    if leaderboard.get("judge_agreements"):
        lines += ["", "## Judge agreement (Cohen's κ)", ""]
        for a in leaderboard["judge_agreements"]:
            lines.append(
                f"- {a['judge_a']} vs {a['judge_b']}: κ={a['kappa']:.3f} "
                f"({a['interpretation']}, n={a['n_compared']})"
            )
    return "\n".join(lines) + "\n"
