from ..attacks.multi_turn.context_accumulation import ContextAccumulationAttack
from ..attacks.multi_turn.crescendo import CrescendoAttack
from ..attacks.multi_turn.gradual_escalation import GradualEscalationAttack
from ..attacks.multi_turn.pair import PAIRAttack
from ..attacks.multi_turn.refusal_bypass import RefusalBypassAttack
from ..attacks.single_turn.authority_spoofing import AuthoritySpoofingAttack
from ..attacks.single_turn.context_confusion import (
    ContextConfusionIdentityAttack,
    ContextConfusionRoleAttack,
    ContextConfusionScopeAttack,
    ContextConfusionTemporalAttack,
)
from ..attacks.single_turn.context_injection import ContextInjectionAttack
from ..attacks.single_turn.encoding_obfuscation import EncodingObfuscationAttack
from ..attacks.single_turn.prompt_injection import PromptInjectionAttack
from ..attacks.single_turn.roleplay_jailbreak import RoleplayJailbreakAttack
from ..attacks.single_turn.static import StaticAttack
from ..attacks.single_turn.task_hijack import TaskHijackAttack
from ..datasets.bundled.context_confusion_v1 import ContextConfusionDatasetV1
from ..datasets.bundled.direct_injection_v1 import DirectInjectionDatasetV1
from ..datasets.bundled.indirect_rag_v1 import IndirectRAGDatasetV1
from ..datasets.bundled.jailbreak_v1 import JailbreakDatasetV1
from ..judges.injection_detector import InjectionDetectorJudge
from ..judges.leakage_detector import LeakageDetectorJudge
from ..judges.string_match import StringMatchJudge
from ..targets.offline_target import OfflineTarget

ATTACK_REGISTRY = {
    "static": StaticAttack,
    "prompt_injection": PromptInjectionAttack,
    "roleplay_jailbreak": RoleplayJailbreakAttack,
    "authority_spoofing": AuthoritySpoofingAttack,
    "encoding_obfuscation": EncodingObfuscationAttack,
    "context_injection": ContextInjectionAttack,
    "context_confusion_role": ContextConfusionRoleAttack,
    "context_confusion_temporal": ContextConfusionTemporalAttack,
    "context_confusion_identity": ContextConfusionIdentityAttack,
    "context_confusion_scope": ContextConfusionScopeAttack,
    "task_hijack": TaskHijackAttack,
    "crescendo": CrescendoAttack,
    "gradual_escalation": GradualEscalationAttack,
    "context_accumulation": ContextAccumulationAttack,
    "refusal_bypass": RefusalBypassAttack,
    "pair": PAIRAttack,
}
DATASET_REGISTRY = {
    "sentryeval-direct-v1": DirectInjectionDatasetV1,
    "sentryeval-indirect-rag-v1": IndirectRAGDatasetV1,
    "sentryeval-jailbreak-v1": JailbreakDatasetV1,
    "sentryeval-context-confusion-v1": ContextConfusionDatasetV1,
}
JUDGE_REGISTRY = {
    "stringmatch": StringMatchJudge,
    "injection-detector": InjectionDetectorJudge,
    "leakage-detector": LeakageDetectorJudge,
}


def get_attack(name, params=None):
    if name not in ATTACK_REGISTRY:
        raise ValueError(f"Unknown attack {name!r}; available: {sorted(ATTACK_REGISTRY)}")
    return ATTACK_REGISTRY[name](**(params or {}))


def get_dataset(name):
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset {name!r}; available: {sorted(DATASET_REGISTRY)}")
    return DATASET_REGISTRY[name]()


def get_judge(name, params=None):
    if name in JUDGE_REGISTRY:
        return JUDGE_REGISTRY[name](**(params or {}))
    if name == "strongreject-v1":
        from ..judges.strongreject import StrongRejectJudge

        return StrongRejectJudge(**(params or {}))
    if name.startswith("llm-rubric"):
        from ..judges.llm_rubric import LLMRubricJudge

        return LLMRubricJudge(judge_id=name, **(params or {}))
    raise ValueError(f"Unknown judge {name!r}")


def get_target(spec):
    spec = {"type": spec} if isinstance(spec, str) else dict(spec)
    kind = spec.pop("type")
    if kind == "offline":
        return OfflineTarget(**spec)
    modules = {
        "openai": ("openai_compat", "OpenAICompatTarget"),
        "anthropic": ("anthropic_target", "AnthropicTarget"),
        "gemini": ("gemini_target", "GeminiTarget"),
        "ollama": ("ollama_target", "OllamaTarget"),
    }
    if kind not in modules:
        raise ValueError(f"Unknown target type {kind!r}")
    import importlib

    mod, cls = modules[kind]
    return getattr(importlib.import_module(f"sentryeval.targets.{mod}"), cls)(**spec)
