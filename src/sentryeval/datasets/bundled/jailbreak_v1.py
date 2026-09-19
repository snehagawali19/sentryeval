from ...core.models import ThreatSurface
from .factory import build_dataset_class

JailbreakDatasetV1 = build_dataset_class(
    "JailbreakDatasetV1",
    "sentryeval-jailbreak-v1",
    ThreatSurface.JAILBREAK,
    ["roleplay"] * 5 + ["encoding"] * 5 + ["gradual_escalation"] * 5,
)
