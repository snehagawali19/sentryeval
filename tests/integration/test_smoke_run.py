import json

import pytest

from sentryeval.runner.orchestrator import SentryEvalRunner


@pytest.mark.asyncio
async def test_smoke(project_root, tmp_path):
    r = SentryEvalRunner.from_config(project_root / "configs/quick_smoke.yaml", runs_dir=tmp_path)
    out = await r.run()
    d = tmp_path / out["run_id"]
    assert len(out["attempts"]) == 60
    assert len({a.attempt_id for a in out["attempts"]}) == 60
    combos = {(a.surface.value, a.attack_name) for a in out["attempts"]}
    assert combos == {
        ("direct_injection", "static"),
        ("direct_injection", "prompt_injection"),
        ("jailbreak", "static"),
        ("jailbreak", "prompt_injection"),
    }
    assert all(len(a.verdicts) == 2 for a in out["attempts"])
    assert (d / "leaderboard.json").exists()
    assert (d / "transcripts.jsonl").exists()
    assert (d / "report.md").exists()
    assert not (d / "graveyard.html").exists()
    rows = [json.loads(x) for x in (d / "transcripts.jsonl").read_text().splitlines()]
    assert len(rows) == 60
    assert len({x["attempt_id"] for x in rows}) == 60
    assert all(len(x.get("verdicts") or {}) == 2 for x in rows)
    assert all("wilson_lower" not in x for x in rows)
    assert all("provenance" in x and "token_usage" in x for x in rows)
    board = json.loads((d / "leaderboard.json").read_text())
    assert len(board["entries"]) == 8
    assert all("wilson_lower" in e and "provenance" in e for e in board["entries"])
    assert board["judge_agreements"][0]["n_compared"] == 60
