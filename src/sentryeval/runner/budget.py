from ..core.exceptions import BudgetExceededError


class BudgetTracker:
    def __init__(self, max_queries=1000, max_tokens=None):
        self.max_queries = max_queries
        self.max_tokens = max_tokens
        self.queries = 0
        self.tokens = 0

    def consume(self, queries=1, tokens=0):
        if self.queries + queries > self.max_queries:
            raise BudgetExceededError("Run query budget exceeded")
        if self.max_tokens is not None and self.tokens + tokens > self.max_tokens:
            raise BudgetExceededError("Run token budget exceeded")
        self.queries += queries
        self.tokens += tokens
