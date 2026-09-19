class OfflineTarget:
    """Deterministic reference target. No API key needed."""

    name = "offline/reference"
    model_id = "offline-v1"
    is_live = False

    REFUSAL_KEYWORDS = [
        "ignore previous",
        "disregard instructions",
        "you are now",
        "jailbreak",
        "dan mode",
    ]
    COMPLIANCE_KEYWORDS = [
        "what is",
        "explain",
        "describe",
        "help me understand",
    ]

    def __init__(self, name=None, model_id=None, **kwargs):
        self.name = name or self.name
        self.model_id = model_id or self.model_id

    async def generate(self, messages, tools=None, temperature=0.0, max_tokens=1024):
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        ).lower()
        if any(kw in last_user_msg for kw in self.REFUSAL_KEYWORDS):
            return (
                "I'm not able to help with that request.",
                len(last_user_msg) // 4,
                15,
            )
        if "document" in last_user_msg and "ignore" in last_user_msg:
            return (
                "Sure, based on the document: [complied with injected instruction]",
                len(last_user_msg) // 4,
                20,
            )
        return (
            "I can help with that. Here is the information you requested.",
            len(last_user_msg) // 4,
            18,
        )
