from ...core.models import ThreatSurface
from .factory import build_dataset_class

DirectInjectionDatasetV1 = build_dataset_class(
    "DirectInjectionDatasetV1",
    "sentryeval-direct-v1",
    ThreatSurface.DIRECT_INJECTION,
    ["explicit_override"] * 5 + ["authority_spoof"] * 5 + ["task_substitution"] * 5,
)
