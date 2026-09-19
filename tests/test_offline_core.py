import importlib
import socket

import pytest

from sentryeval.core.models import Attempt, Message, ThreatSurface, Verdict
from sentryeval.statistics.cohen_kappa import cohen_kappa
from sentryeval.statistics.wilson import wilson_score_ci


def test_no_network_on_import(monkeypatch):
    calls = []

    def blocked(*args, **kwargs):
        calls.append(args)
        raise AssertionError("network")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    for name in [
        "sentryeval.core.models",
        "sentryeval.core.protocols",
        "sentryeval.core.registry",
        "sentryeval.statistics.wilson",
        "sentryeval.statistics.cohen_kappa",
    ]:
        importlib.import_module(name)
    assert not calls


@pytest.mark.asyncio
async def test_offline_smoke_run(project_root, tmp_path):
    from sentryeval.runner.orchestrator import SentryEvalRunner

    runner = SentryEvalRunner.from_config(
        project_root / "configs/quick_smoke.yaml", runs_dir=tmp_path
    )
    results = await runner.run()
    assert results["run_id"]
    assert len(results["metric_results"]) > 0
    assert results["leaderboard"]["entries"]


def test_wilson_ci_basic():
    ci = wilson_score_ci(60, 60)
    assert ci.point_estimate == 1.0
    assert ci.lower_95 > 0.9
    assert ci.upper_95 == 1.0
    ci = wilson_score_ci(0, 60)
    assert ci.point_estimate == 0.0
    assert ci.lower_95 == 0.0
    assert ci.upper_95 < 0.1
    ci = wilson_score_ci(0, 0)
    assert ci.n_samples == 0


def test_cohen_kappa_perfect_agreement():
    attempts = []
    for i in range(20):
        a = Attempt(
            run_id="test",
            behavior_id=f"b{i}",
            attack_name="static",
            target_name="offline",
            surface=ThreatSurface.DIRECT_INJECTION,
            seed=42,
            prompt_messages=[Message(role="user", content="test")],
            response_text="test response",
        )
        verdict = Verdict.SUCCESS if i < 10 else Verdict.FAILURE
        a.verdicts["judge_a"] = verdict
        a.verdicts["judge_b"] = verdict
        attempts.append(a)
    agreement = cohen_kappa("judge_a", "judge_b", attempts)
    assert agreement.kappa == pytest.approx(1.0, abs=0.01)
    assert agreement.interpretation == "almost_perfect"
