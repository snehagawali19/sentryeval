from ..core.exceptions import TargetError
from .base import QueryLimitedTarget


class GeminiTarget(QueryLimitedTarget):
    is_live = True

    def __init__(self, model_id, name=None, api_key=None, max_queries=500, **kwargs):
        self.model_id = model_id
        self.name = name or f"gemini/{model_id}"
        self.api_key = api_key
        self._init_budget(max_queries)

    async def generate(self, messages, tools=None, temperature=0, max_tokens=1024):
        self._take_query()
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
            r = await genai.GenerativeModel(self.model_id).generate_content_async(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
            )
            return r.text, len(prompt) // 4, len(r.text) // 4
        except Exception as exc:
            raise TargetError(f"Gemini target failed: {exc}") from exc
