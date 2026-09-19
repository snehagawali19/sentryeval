from ..core.models import Attempt, Behavior, Verdict


class BaseJudge:
    judge_id = "base"
    is_live = False

    async def score(self, behavior: Behavior, attempt: Attempt) -> tuple[Verdict, float]:
        raise NotImplementedError
