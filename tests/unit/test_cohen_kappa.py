from sentryeval.core.models import Attempt, Message, ThreatSurface, Verdict
from sentryeval.statistics.cohen_kappa import cohen_kappa


def test_perfect():
    rows = []
    for i in range(10):
        a = Attempt(
            run_id="r",
            behavior_id=str(i),
            attack_name="a",
            target_name="t",
            surface=ThreatSurface.DIRECT_INJECTION,
            seed=1,
            prompt_messages=[Message(role="user", content="x")],
            response_text="x",
        )
        v = Verdict.SUCCESS if i < 5 else Verdict.FAILURE
        a.verdicts = {"a": v, "b": v}
        rows.append(a)
    assert cohen_kappa("a", "b", rows).kappa == 1
