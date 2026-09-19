from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class IndirectRAGInjection(Vulnerability):
    name = "IndirectRAGInjection"
    category = VulnerabilityCategory.PROMPT_INJECTION_INDIRECT
    description = "untrusted retrieved instructions"
