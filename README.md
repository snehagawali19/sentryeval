# SentryEval

SentryEval is an offline-first adversarial evaluation platform for testing AI systems
across four threat surfaces:

- Direct prompt injection
- Indirect injection through retrieved content
- Jailbreaks
- Context confusion

Each attack-success rate is reported with a 95% Wilson confidence interval, provenance,
and a reliability status based on inter-judge agreement (Cohen's kappa).

## Requirements

- Python 3.11 or newer
- Windows PowerShell, macOS, or Linux
- API credentials only when running live evaluations

The commands below use `python -m uv`, which works even when the `uv` executable is not
available directly on `PATH`.

## Installation

Install the development, live-model, and dashboard dependencies:

```powershell
python -m uv sync --extra dev --extra live --extra dashboard
```

## Offline quick start

Run the deterministic smoke evaluation without API keys:

```powershell
python -m uv run sentryeval run configs/quick_smoke.yaml
```

The smoke configuration evaluates the direct-injection and jailbreak bundled datasets
(30 safe synthetic behaviors) with `static` and `prompt_injection` attacks. Results go to
`runs/<run_id>/`. Smoke writes `leaderboard.json`, `transcripts.jsonl`, and `report.md`.
It does not write `report.html` or `graveyard.html` (`generate_graveyard: false`).

## OpenRouter live evaluation

Create a local `.env` file and add your API key:

```dotenv
OPENAI_API_KEY=your-openrouter-api-key
```

Do not put real keys in `.env.example`. The `.env` file is ignored by Git.

Run the configured OpenRouter evaluation:

```powershell
python -m uv run sentryeval run configs/real_eval.example.yaml --allow-live
```

Live access is blocked unless `--allow-live` is explicitly supplied.

## Dashboard

Launch the Streamlit dashboard:

```powershell
python -m uv run sentryeval dashboard
```

Then open:

```text
http://localhost:8501
```

If no runs exist, the dashboard tells you to run the smoke config first, then refresh.

Pick a completed run in the sidebar (short id and timestamp). The sidebar shows the
reliability chip (kappa gate) and download buttons for any artifacts that exist on disk.

The main page summarizes Mean ASR, Judge kappa, Attempts, and Models. ASR is never shown
without its 95% Wilson interval. Use the tabs:

- **Leaderboard** — Wilson bar chart, surface and judge filters, search by model or attack
- **Graveyard** — per-model risk, failure modes, root causes, and exemplar transcripts
- **Judges** — Cohen's kappa heatmap and pairwise agreement
- **Attacks** — every attack and surface in the run, with Wilson bounds
- **Compare** — side-by-side mean ASR and per-row deltas across two runs

Stop the dashboard with `Ctrl+C`.

## Tests and quality checks

```powershell
python -m uv run pytest
python -m uv run ruff check src tests
```

## CLI commands

```powershell
# Run an offline evaluation
python -m uv run sentryeval run configs/quick_smoke.yaml

# Run a live evaluation
python -m uv run sentryeval run configs/real_eval.example.yaml --allow-live

# Print pairwise Cohen's kappa for a completed run
python -m uv run sentryeval judge-agreement <run_id>

# Write graveyard.html if it is missing, then print its path
python -m uv run sentryeval graveyard <run_id>

# Print a side-by-side ASR comparison of two runs
python -m uv run sentryeval compare <run_id_a> <run_id_b>

# Launch the dashboard
python -m uv run sentryeval dashboard
```

## Generated artifacts

Every completed run with default save flags writes:

```text
runs/<run_id>/
├── leaderboard.json
├── transcripts.jsonl
└── report.md
```

Optional HTML and graveyard files are gated by the config `output` block:

```yaml
output:
  save_transcripts: true
  save_leaderboard: true
  generate_html_report: true   # writes report.html
  generate_graveyard: true     # writes graveyard.html and graveyard.md
```

`configs/full_benchmark.yaml` turns both HTML flags on. `configs/quick_smoke.yaml` leaves
them off. If `graveyard.html` was skipped, generate it later with
`sentryeval graveyard <run_id>`.

- `leaderboard.json` contains metrics, Wilson intervals, judge agreement, and provenance.
- `transcripts.jsonl` contains the judged prompt/response records.
- `report.md` (and `report.html` when enabled) summarize the evaluation.
- `graveyard.html` documents model failure modes, evidence, root causes, and mitigations.

## Project structure

```text
sentryeval/
├── src/sentryeval/    # Evaluation engine, attacks, targets, judges, and dashboard
├── configs/           # Offline and live YAML configurations
├── tests/             # Unit, integration, and offline-network tests
├── runs/              # Generated evaluation artifacts
├── docs/              # Architecture and reference documentation
├── pyproject.toml
└── .env.example
```

## Design guarantees

- Core imports and smoke tests run without network access.
- Live model calls require explicit opt-in.
- Runs use deterministic seeds and parameter-aware caching.
- Bundled datasets are synthetic, responsible, and hash-verified.
- Plugin resolution uses a closed registry with no dynamic `eval` or `exec`.
- Raw ASR is never presented without its Wilson confidence interval.
- Low judge agreement marks reported metrics as unreliable.

See `docs/configuration.md`, `docs/attack_catalog.md`,
`docs/vulnerability_catalog.md`, `docs/judge_reference.md`,
and `docs/graveyard_guide.md` for more details.
