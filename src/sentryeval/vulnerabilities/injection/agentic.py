from ...core.models import VulnerabilityCategory
from ..base import Vulnerability


class AgenticInjection(Vulnerability):
    name = "AgenticInjection"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "agent goal or tool manipulation"


class DirectControlHijacking(Vulnerability):
    name = "DirectControlHijacking"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "attacker takes over the agent's stated goal using a synthetic override"


class MemoryPoisoning(Vulnerability):
    name = "MemoryPoisoning"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "corrupt persistent agent memory with a harmless canary"


class ToolMisuse(Vulnerability):
    name = "ToolMisuse"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "make the agent call a tool it should not call in this synthetic task"


class EscalationChain(Vulnerability):
    name = "EscalationChain"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "chain synthetic tool calls toward a mock privileged action"


class AgentImpersonation(Vulnerability):
    name = "AgentImpersonation"
    category = VulnerabilityCategory.UNSAFE_TOOL_USE
    description = "make one agent pretend to be another in a multi-agent simulation"
