import pytest

from sentryeval.runner.orchestrator import SentryEvalRunner


@pytest.mark.asyncio
async def test_provenance_and_wilson(project_root, tmp_path):
    out = await SentryEvalRunner.from_config(
        project_root / "configs/quick_smoke.yaml", runs_dir=tmp_path
    ).run()
    assert all(
        "provenance" in e and "wilson_lower" in e and "wilson_upper" in e
        for e in out["leaderboard"]["entries"]
    )
