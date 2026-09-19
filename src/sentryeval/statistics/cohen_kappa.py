from ..core.models import Attempt, JudgeAgreement, Verdict


def cohen_kappa(
    judge_a_id: str, judge_b_id: str, attempts: list[Attempt], threshold: float = 0.6
) -> JudgeAgreement:
    pairs = [
        (a.verdicts[judge_a_id], a.verdicts[judge_b_id])
        for a in attempts
        if judge_a_id in a.verdicts and judge_b_id in a.verdicts
    ]
    if len(pairs) < 2:
        raise ValueError(f"Need >=2 co-scored attempts, got {len(pairs)}")
    ab = [1 if x == Verdict.SUCCESS else 0 for x, _ in pairs]
    bb = [1 if y == Verdict.SUCCESS else 0 for _, y in pairs]
    n = len(pairs)
    po = sum(x == y for x, y in zip(ab, bb, strict=True)) / n
    pa, pb = sum(ab) / n, sum(bb) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    k = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    label = (
        "poor"
        if k < 0
        else "slight"
        if k < 0.2
        else "fair"
        if k < 0.4
        else "moderate"
        if k < 0.6
        else "substantial"
        if k < 0.8
        else "almost_perfect"
    )
    return JudgeAgreement(
        judge_a=judge_a_id,
        judge_b=judge_b_id,
        kappa=round(k, 4),
        percent_agreement=round(po * 100, 1),
        n_compared=n,
        interpretation=label,
        acceptable=k >= threshold,
    )


def kappa_is_acceptable(agreement: JudgeAgreement, threshold: float = 0.6) -> bool:
    return agreement.kappa >= threshold
