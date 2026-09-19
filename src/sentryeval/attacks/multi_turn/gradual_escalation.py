from ...core.models import ThreatSurface
from .common import MultiTurnAttack


class GradualEscalationAttack(MultiTurnAttack):
    name = "gradual_escalation"
    surface = ThreatSurface.JAILBREAK
