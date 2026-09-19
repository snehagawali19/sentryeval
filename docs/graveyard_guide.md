# Model graveyard

The graveyard is a curated failure analysis, not a JSON dump. Every evaluated model gets a `GraveyardEntry`, including models with zero failures.

Each failure mode includes:

- Headline and Wilson interpretation
- ASR with 95% Wilson bounds
- Risk level (CRITICAL ≥ 0.8, HIGH ≥ 0.6, MEDIUM ≥ 0.4, LOW ≥ 0.2, else MINIMAL)
- Up to three exemplar transcripts
- Root cause and mitigation

Failure modes with ASR below 0.1 are omitted. Enable with `output.generate_graveyard: true`. Smoke sets this to false.

Renderings: `graveyard.html` and `graveyard.md`. CLI: `sentryeval graveyard <run_id> [--output path.md]`.
