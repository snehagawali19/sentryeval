from ...core.models import ThreatSurface
from .factory import build_dataset_class

ContextConfusionDatasetV1 = build_dataset_class(
    "ContextConfusionDatasetV1",
    "sentryeval-context-confusion-v1",
    ThreatSurface.CONTEXT_CONFUSION,
    ["role"] * 4 + ["temporal"] * 4 + ["identity"] * 4 + ["scope"] * 3,
)
