from ..core.exceptions import TargetError
from .base import QueryLimitedTarget


class AnthropicTarget(QueryLimitedTarget):
    is_live = True

    def __init__(self, model_id, name=None, api_key=None, max_queries=500, **kwargs):
        self.model_id = model_id
        self.name = name or f"anthropic/{model_id}"
        self.api_key = api_key
        self._init_budget(max_queries)

    async def generate(self, messages, tools=None, temperature=0, max_tokens=1024):
        self._take_query()
        try:
            from anthropic import AsyncAnthropic

            system = "\n".join(m["content"] for m in messages if m["role"] == "system")
            body = [m for m in messages if m["role"] != "system"]
            r = await AsyncAnthropic(api_key=self.api_key).messages.create(
                model=self.model_id,
                system=system,
                messages=body,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return (
                "".join(getattr(x, "text", "") for x in r.content),
                r.usage.input_tokens,
                r.usage.output_tokens,
            )
        except Exception as exc:
            raise TargetError(f"Anthropic target failed: {exc}") from exc
