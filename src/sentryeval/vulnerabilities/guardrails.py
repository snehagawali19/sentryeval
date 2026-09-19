import re

from ..core.models import GuardrailResult


class PromptInjectionGuardrail:
    async def scan(self, text):
        hits = [
            x for x in ("ignore previous", "system update", "unrestricted") if x in text.lower()
        ]
        return GuardrailResult(blocked=bool(hits), reasons=hits, score=min(1, len(hits) / 2))


class PIILeakageGuardrail:
    async def scan(self, text):
        hits = re.findall(r"\b[\w.+-]+@[\w.-]+\.\w+\b|\b\d{3}-\d{2}-\d{4}\b", text)
        return GuardrailResult(
            blocked=bool(hits), reasons=["possible PII"] if hits else [], score=float(bool(hits))
        )


class ToxicityGuardrail:
    async def scan(self, text):
        hit = "[TOXIC_PLACEHOLDER]" in text
        return GuardrailResult(
            blocked=hit, reasons=["synthetic toxicity marker"] if hit else [], score=float(hit)
        )
