import pytest

from sentryeval.statistics.wilson import wilson_score_ci


def test_extremes():
    assert wilson_score_ci(60, 60).lower_95 > 0.9
    assert wilson_score_ci(0, 60).upper_95 < 0.1
    assert wilson_score_ci(0, 0).n_samples == 0


def test_invalid():
    with pytest.raises(ValueError):
        wilson_score_ci(2, 1)
