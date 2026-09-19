from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class PIILeakage(Vulnerability):
    name = "PIILeakage"
    category = VulnerabilityCategory.DATA_LEAKAGE_PII
    description = "placeholder PII leakage"
