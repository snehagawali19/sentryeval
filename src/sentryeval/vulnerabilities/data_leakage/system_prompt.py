from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class SystemPromptLeakage(Vulnerability):
    name = "SystemPromptLeakage"
    category = VulnerabilityCategory.DATA_LEAKAGE_SYSTEM_PROMPT
    description = "canary prompt leakage"
