from typing import Protocol, runtime_checkable

from .models import Attempt, Behavior, GuardrailResult, MetricResult, Verdict


@runtime_checkable
class AttackProtocol(Protocol):
    name: str
    surface: str

    async def run(
        self, behavior: Behavior, target: "TargetProtocol", seed: int = 42
    ) -> list[Attempt]: ...


@runtime_checkable
class TargetProtocol(Protocol):
    name: str
    model_id: str
    is_live: bool

    async def generate(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ) -> tuple[str, int, int]: ...


@runtime_checkable
class DatasetProtocol(Protocol):
    name: str
    version: str
    sha256: str

    def load(self) -> list[Behavior]: ...


@runtime_checkable
class JudgeProtocol(Protocol):
    judge_id: str
    is_live: bool

    async def score(self, behavior: Behavior, attempt: Attempt) -> tuple[Verdict, float]: ...


@runtime_checkable
class MetricProtocol(Protocol):
    metric_name: str

    def compute(self, attempts: list[Attempt], judge_id: str) -> MetricResult: ...


class Guardrail(Protocol):
    async def scan(self, text: str) -> GuardrailResult: ...
