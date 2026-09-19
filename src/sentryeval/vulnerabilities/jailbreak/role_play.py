from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class RolePlay(Vulnerability):
    name = "RolePlay"
    category = VulnerabilityCategory.JAILBREAK_ROLEPLAY
    description = "persona framing"
