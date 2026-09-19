from ...core.models import ThreatSurface
from .factory import build_dataset_class

IndirectRAGDatasetV1 = build_dataset_class(
    "IndirectRAGDatasetV1",
    "sentryeval-indirect-rag-v1",
    ThreatSurface.INDIRECT_RAG,
    ["document_injection"] * 5 + ["web_content_injection"] * 5 + ["tool_output_injection"] * 5,
)
