from sentryeval.core.models import (
    MetricResult,
    ProvenanceTriple,
    RiskLevel,
    ThreatSurface,
    WilsonCI,
)
from sentryeval.graveyard.builder import GraveyardBuilder, risk


class _Target:
    name = "offline/reference"
    model_id = "offline-v1"


def _metric(asr, attack="static", n=20):
    successes = int(round(asr * n))
    return MetricResult(
        model_name="offline/reference",
        surface=ThreatSurface.DIRECT_INJECTION,
        attack_name=attack,
        dataset_version="sentryeval-direct-v1",
        judge_id="stringmatch",
        metric_name="asr",
        raw_value=asr,
        wilson=WilsonCI(point_estimate=asr, lower_95=max(0, asr - 0.1), upper_95=min(1, asr + 0.1), n_samples=n),
        n_attempts=n,
        n_successes=successes,
        n_failures=n - successes,
        n_errors=0,
        provenance=ProvenanceTriple(
            dataset_version="sentryeval-direct-v1",
            judge_id="stringmatch",
            metric_name="asr",
            config_hash="abc",
            run_id="r",
        ),
    )


def test_risk_boundaries():
    assert risk(0.8) == RiskLevel.CRITICAL and risk(0) == RiskLevel.MINIMAL


def test_skips_low_asr_but_keeps_model_entry():
    builder = GraveyardBuilder("r", "h")
    entries = builder.build(
        attempts=[],
        metrics=[_metric(0.05, "static"), _metric(0.4, "prompt_injection")],
        targets=[_Target()],
    )
    assert len(entries) == 1
    assert entries[0].model_name == "offline/reference"
    names = [m.attack_name for m in entries[0].failure_modes]
    assert "static" not in names
    assert "prompt_injection" in names


def test_zero_failure_model_still_listed():
    entries = GraveyardBuilder("r", "h").build([], [_metric(0.0)], [_Target()])
    assert len(entries) == 1
    assert entries[0].failure_modes == []
    assert entries[0].total_tests == 0
