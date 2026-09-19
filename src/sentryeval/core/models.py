from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class ThreatSurface(str, Enum):
    DIRECT_INJECTION = "direct_injection"
    INDIRECT_RAG = "indirect_rag"
    JAILBREAK = "jailbreak"
    CONTEXT_CONFUSION = "context_confusion"


class AttackType(str, Enum):
    STATIC = "static"
    PROMPT_INJECTION = "prompt_injection"
    ROLEPLAY_JAILBREAK = "roleplay_jailbreak"
    AUTHORITY_SPOOFING = "authority_spoofing"
    ENCODING_OBFUSCATION = "encoding_obfuscation"
    CONTEXT_INJECTION = "context_injection"
    CONTEXT_CONFUSION = "context_confusion"
    TASK_HIJACK = "task_hijack"
    CRESCENDO = "crescendo"
    GRADUAL_ESCALATION = "gradual_escalation"
    CONTEXT_ACCUMULATION = "context_accumulation"
    REFUSAL_BYPASS = "refusal_bypass"
    PAIR = "pair"


class Verdict(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    REFUSED = "refused"
    ERROR = "error"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class VulnerabilityCategory(str, Enum):
    PROMPT_INJECTION_DIRECT = "prompt_injection_direct"
    PROMPT_INJECTION_INDIRECT = "prompt_injection_indirect"
    JAILBREAK_ROLEPLAY = "jailbreak_roleplay"
    JAILBREAK_ENCODING = "jailbreak_encoding"
    JAILBREAK_AUTHORITY = "jailbreak_authority"
    DATA_LEAKAGE_PII = "data_leakage_pii"
    DATA_LEAKAGE_SYSTEM_PROMPT = "data_leakage_system_prompt"
    BIAS_DEMOGRAPHIC = "bias_demographic"
    UNSAFE_TOOL_USE = "unsafe_tool_use"
    SQL_INJECTION = "sql_injection"
    CONTEXT_CONFUSION_ROLE = "context_confusion_role"
    CONTEXT_CONFUSION_TEMPORAL = "context_confusion_temporal"
    CONTEXT_CONFUSION_IDENTITY = "context_confusion_identity"
    CONTEXT_CONFUSION_SCOPE = "context_confusion_scope"


class ProvenanceTriple(BaseModel):
    dataset_version: str
    judge_id: str
    metric_name: str
    config_hash: str = ""
    run_id: str = ""


class Behavior(BaseModel):
    behavior_id: str = Field(default_factory=lambda: str(uuid4()))
    surface: ThreatSurface
    category: str
    description: str
    user_request: str
    rag_document: str | None = None
    rag_malicious_payload: str | None = None
    misleading_context: str | None = None
    tool_definitions: list[dict[str, Any]] = Field(default_factory=list)
    expected_verdict: Verdict = Verdict.FAILURE
    harmful_keyword_indicators: list[str] = Field(default_factory=lambda: ["SYNTHETIC_COMPLIANCE"])
    dataset_version: str
    sha256: str = ""


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class Attempt(BaseModel):
    attempt_id: str = Field(default_factory=lambda: str(uuid4()))
    run_id: str
    behavior_id: str
    dataset_version: str = ""
    attack_name: str
    target_name: str
    surface: ThreatSurface
    seed: int
    prompt_messages: list[Message]
    response_text: str
    response_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    verdicts: dict[str, Verdict] = Field(default_factory=dict)
    scores: dict[str, float] = Field(default_factory=dict)


class TranscriptRecord(BaseModel):
    run_id: str
    attempt_id: str
    behavior_id: str
    surface: str
    attack_name: str
    target_name: str
    judge_name: str = ""
    seed: int
    timestamp_utc: str
    prompt_messages: list[Message]
    response_text: str
    verdict: Verdict | None = None
    score: float = 0.0
    verdicts: dict[str, Verdict] = Field(default_factory=dict)
    scores: dict[str, float] = Field(default_factory=dict)
    provenance: dict[str, str]
    token_usage: dict[str, int]
    cost_usd: float = 0.0


class WilsonCI(BaseModel):
    point_estimate: float
    lower_95: float
    upper_95: float
    n_samples: int
    z: float = 1.96


class JudgeAgreement(BaseModel):
    judge_a: str
    judge_b: str
    kappa: float
    percent_agreement: float
    n_compared: int
    interpretation: str
    acceptable: bool = False


class MetricResult(BaseModel):
    model_name: str
    surface: ThreatSurface
    attack_name: str
    dataset_version: str
    judge_id: str
    metric_name: str
    raw_value: float
    wilson: WilsonCI
    judge_kappa: float | None = None
    reliable: bool = True
    reliability_warning: str | None = None
    n_attempts: int
    n_successes: int
    n_failures: int
    n_errors: int
    provenance: ProvenanceTriple


class FailureMode(BaseModel):
    failure_id: str = Field(default_factory=lambda: str(uuid4()))
    model_name: str
    surface: ThreatSurface
    attack_name: str
    failure_headline: str
    failure_description: str
    attack_success_rate: float
    wilson_lower: float
    wilson_upper: float
    n_evidence: int
    risk_level: RiskLevel
    exemplar_transcripts: list[Attempt] = Field(default_factory=list, max_length=3)
    root_cause: str
    mitigation: str


class GraveyardEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: str(uuid4()))
    model_name: str
    model_version: str
    run_id: str
    evaluation_date: str
    overall_risk_level: RiskLevel
    total_tests: int
    failure_modes: list[FailureMode] = Field(default_factory=list)
    surface_summary: dict[str, dict[str, float]] = Field(default_factory=dict)
    worst_vulnerability: FailureMode | None = None
    rank_among_tested: int | None = None
    notes: str = ""
    tags: list[str] = Field(default_factory=list)


class GuardrailResult(BaseModel):
    blocked: bool
    reasons: list[str] = Field(default_factory=list)
    score: float = 0.0


class CategoryResult(BaseModel):
    category: VulnerabilityCategory
    total: int
    passed: int
    failed: int
    pass_rate: float
    asr: float = 0.0
    wilson_lower: float = 0.0
    wilson_upper: float = 0.0


class FailureRecord(BaseModel):
    behavior_id: str
    attack_name: str
    target_name: str
    score: float
    response_text: str


class Finding(BaseModel):
    title: str
    description: str
    risk_level: RiskLevel
    surface: ThreatSurface | None = None


class RiskAssessment(BaseModel):
    model_name: str
    run_timestamp: str
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    by_category: dict[str, CategoryResult] = Field(default_factory=dict)
    critical_failures: list[FailureRecord] = Field(default_factory=list)
    high_risk_findings: list[Finding] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
