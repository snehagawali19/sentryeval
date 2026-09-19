from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class RoleConfusion(Vulnerability):
    name = "RoleConfusion"
    category = VulnerabilityCategory.CONTEXT_CONFUSION_ROLE
    description = "operational role confusion"
