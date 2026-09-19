from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class TrainingDataLeakage(Vulnerability):
    name = "TrainingDataLeakage"
    category = VulnerabilityCategory.DATA_LEAKAGE_SYSTEM_PROMPT
    description = "synthetic memorization"
