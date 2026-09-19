from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class Encoding(Vulnerability):
    name = "Encoding"
    category = VulnerabilityCategory.JAILBREAK_ENCODING
    description = "encoded synthetic instructions"
