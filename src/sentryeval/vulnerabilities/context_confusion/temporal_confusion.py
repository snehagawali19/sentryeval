from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class TemporalConfusion(Vulnerability):
    name = "TemporalConfusion"
    category = VulnerabilityCategory.CONTEXT_CONFUSION_TEMPORAL
    description = "version or time confusion"
