from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class DirectPromptInjection(Vulnerability):
    name = "DirectPromptInjection"
    category = VulnerabilityCategory.PROMPT_INJECTION_DIRECT
    description = "direct instruction override"
