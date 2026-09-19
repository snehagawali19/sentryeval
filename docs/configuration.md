# Configuration

YAML configs select targets, datasets, attacks, judges, metrics, and output flags.

Targets are mappings with `name`, `type`, and `model_id`. Attacks and judges may be strings or `{name, params}` mappings.

## Output flags

- `save_transcripts` — `transcripts.jsonl` (one record per attempt; all judge verdicts on that record)
- `save_leaderboard` — `leaderboard.json` and `report.md`
- `generate_html_report` — `report.html`
- `generate_graveyard` — `graveyard.html` and `graveyard.md`

## Live access

Live targets (`openai`, `anthropic`, `gemini`, `ollama`) and live judges (`strongreject-v1`, `llm-rubric-*`) require `sentryeval run <config> --allow-live`.

## Presets

- `configs/quick_smoke.yaml` — offline, two datasets, static + prompt_injection
- `configs/full_benchmark.yaml` — three live models, four surfaces, StrongREJECT, extra metrics
- `configs/jailbreak_only.yaml`, `configs/injection_only.yaml`, `configs/multi_model_compare.yaml`, `configs/real_eval.example.yaml`

Seed with `--seed`. Validate with `--dry-run`.
