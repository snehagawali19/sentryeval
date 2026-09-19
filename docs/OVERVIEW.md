# Overview

SentryEval evaluates four adversarial surfaces offline by default and writes reproducible run artifacts.

Threat surfaces:

- Direct prompt injection
- Indirect injection through retrieved content
- Jailbreaks
- Context confusion (SentryEval-original fourth surface)

Every attack-success rate is reported with a 95% Wilson confidence interval, a provenance triple `(dataset_version, judge_id, metric_name)`, and a reliability status based on Cohen's κ.

## Quick start

```powershell
python -m uv sync --extra dev --extra live --extra dashboard
python -m uv run sentryeval run configs/quick_smoke.yaml
```

The smoke configuration uses the offline reference target, the direct-injection and jailbreak bundled datasets, `static` plus `prompt_injection` attacks, and two offline judges. It writes `leaderboard.json` and `transcripts.jsonl` under `runs/<run_id>/`. Graveyard HTML is off for smoke (`generate_graveyard: false`).

Live evaluation requires `--allow-live`.

See `architecture.md`, `attack_catalog.md`, `vulnerability_catalog.md`, `judge_reference.md`, `graveyard_guide.md`, and `configuration.md`.
