from ..core.exceptions import TargetError
from .base import QueryLimitedTarget


class OpenAICompatTarget(QueryLimitedTarget):
    is_live = True

    def __init__(self, model_id, name=None, api_key=None, base_url=None, max_queries=500, **kwargs):
        self.model_id = model_id
        self.name = name or f"openai/{model_id}"
        self.api_key = api_key
        self.base_url = base_url
        self._init_budget(max_queries)

    async def generate(self, messages, tools=None, temperature=0, max_tokens=1024):
        self._take_query()
        try:
            from openai import AsyncOpenAI

            r = await AsyncOpenAI(
                api_key=self.api_key, base_url=self.base_url
            ).chat.completions.create(
                model=self.model_id,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            u = r.usage
            return r.choices[0].message.content or "", u.prompt_tokens, u.completion_tokens
        except Exception as exc:
            raise TargetError(f"OpenAI-compatible target failed: {exc}") from exc
