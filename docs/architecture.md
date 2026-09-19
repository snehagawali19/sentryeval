# Architecture

SentryEval is an `Attack × Target × Dataset × Judge × Metric` matrix. Each axis is a `Protocol` (structural subtyping, not ABC). Plugins resolve through a closed registry dictionary; there is no `eval` or `exec`.

```text
YAML config
  -> SentryEvalRunner
  -> Attack x Target x Behavior (parameter-aware cache)
  -> Attempts
  -> Judges
  -> transcripts.jsonl (one line per attempt; verdicts/scores on the same record)
  -> Cohen's kappa gate
  -> ASR and configured metrics with Wilson 95% CIs
  -> leaderboard.json, report.md, report.html, graveyard.html
```

Reproducibility contract:

- Hash-pinned datasets (SHA-256 verified on load)
- Deterministic seeds (`random`, `numpy`, temperature 0)
- Cache keyed on attack, target, dataset hash, behavior id, seed, and hyperparameters

Live targets and live judges are blocked unless the CLI receives `--allow-live`.
