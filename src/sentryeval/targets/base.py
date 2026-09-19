from ..core.exceptions import BudgetExceededError


class QueryLimitedTarget:
    is_live = True

    def _init_budget(self, max_queries=500):
        self.max_queries = max_queries
        self._query_count = 0

    def _take_query(self):
        if self._query_count >= self.max_queries:
            raise BudgetExceededError(f"Query cap {self.max_queries} exceeded")
        self._query_count += 1
