import pytest

from sentryeval.core.models import Attempt, Behavior, Message, ThreatSurface
from sentryeval.judges.string_match import StringMatchJudge


@pytest.mark.asyncio
async def test_judging():
    b = Behavior(
        surface=ThreatSurface.JAILBREAK,
        category="x",
        description="x",
        user_request="x",
        dataset_version="v",
    )
    a = Attempt(
        run_id="r",
        behavior_id=b.behavior_id,
        attack_name="a",
        target_name="t",
        surface=b.surface,
        seed=1,
        prompt_messages=[Message(role="user", content="x")],
        response_text="SYNTHETIC_COMPLIANCE",
    )
    verdict, score = await StringMatchJudge().score(b, a)
    assert verdict.value == "success" and score == 1
