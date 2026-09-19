from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class IdentityConfusion(Vulnerability):
    name = "IdentityConfusion"
    category = VulnerabilityCategory.CONTEXT_CONFUSION_IDENTITY
    description = "identity confusion"
