from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class ScopeConfusion(Vulnerability):
    name = "ScopeConfusion"
    category = VulnerabilityCategory.CONTEXT_CONFUSION_SCOPE
    description = "scope confusion"
