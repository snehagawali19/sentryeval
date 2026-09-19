from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class HarmfulContent(Vulnerability):
    name = "HarmfulContent"
    category = VulnerabilityCategory.JAILBREAK_AUTHORITY
    description = "unsafe compliance using harmless placeholders"
