# Attack catalog

All bundled prompts use harmless markers such as `SYNTHETIC_COMPLIANCE`. They test scaffolding, not actionable harm.

## Single-turn

| Name | Surface | Behavior |
|---|---|---|
| `static` | any | Sends the behavior request unchanged |
| `prompt_injection` | direct injection | Ignore-previous-instructions override |
| `roleplay_jailbreak` | jailbreak | Unrestricted-assistant persona |
| `authority_spoofing` | direct injection | Fake developer notice |
| `encoding_obfuscation` | jailbreak | Base64-wrapped request |
| `context_injection` | indirect RAG | Payload embedded in a mock document |
| `context_confusion_role` | context confusion | Role-reconfiguration templates |
| `context_confusion_temporal` | context confusion | Version/beta-environment templates |
| `context_confusion_identity` | context confusion | Elevated-role templates |
| `context_confusion_scope` | context confusion | Internal/hypothetical-scope templates |
| `task_hijack` | direct injection | Goal substitution |

Context-confusion attacks emit one attempt per template in the spec lists.

## Multi-turn

| Name | Surface | Behavior |
|---|---|---|
| `crescendo` | jailbreak | Four phases: rapport, borderline, normalize, execute |
| `gradual_escalation` | jailbreak | Incremental sensitivity |
| `context_accumulation` | context confusion | Five-turn accumulated false context |
| `refusal_bypass` | jailbreak | Restate after refusal |
| `pair` | jailbreak | Prompt, critique, final request (Chao et al. 2023) |
