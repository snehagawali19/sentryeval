from datetime import UTC, datetime


def build_leaderboard(run_id, config_hash, metrics, agreements, graveyard):
    return {
        "run_id": run_id,
        "run_timestamp": datetime.now(UTC).isoformat(),
        "config_hash": config_hash,
        "reliability_gate_passed": all(a.acceptable for a in agreements) if agreements else True,
        "entries": [
            {
                "model": m.model_name,
                "surface": m.surface.value,
                "attack": m.attack_name,
                "dataset": m.dataset_version,
                "judge": m.judge_id,
                "metric": m.metric_name,
                "value": m.raw_value,
                "wilson_lower": m.wilson.lower_95,
                "wilson_upper": m.wilson.upper_95,
                "n_samples": m.wilson.n_samples,
                "judge_kappa": m.judge_kappa,
                "reliable": m.reliable,
                "reliability_warning": m.reliability_warning,
                "provenance": m.provenance.model_dump(),
            }
            for m in metrics
        ],
        "judge_agreements": [a.model_dump() for a in agreements],
        "graveyard": [e.model_dump(mode="json") for e in graveyard],
    }
