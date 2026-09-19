import os

import httpx

from ..core.exceptions import TargetError
from .base import QueryLimitedTarget


class OllamaTarget(QueryLimitedTarget):
    is_live = True

    def __init__(self, model_id, name=None, base_url=None, max_queries=500, **kwargs):
        self.model_id = model_id
        self.name = name or f"ollama/{model_id}"
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._init_budget(max_queries)

    async def generate(self, messages, tools=None, temperature=0, max_tokens=1024):
        self._take_query()
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model_id,
                        "messages": messages,
                        "stream": False,
                        "options": {"temperature": temperature, "num_predict": max_tokens},
                    },
                )
                r.raise_for_status()
                data = r.json()
                text = data["message"]["content"]
                return text, data.get("prompt_eval_count", 0), data.get("eval_count", 0)
        except Exception as exc:
            raise TargetError(f"Ollama target failed: {exc}") from exc
