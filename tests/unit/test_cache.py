from sentryeval.runner.cache import ResultCache


def test_behavior_and_hyperparameter_aware(tmp_path):
    c = ResultCache(tmp_path)
    a = c.make_key("x", "t", "h", "b1", 42, hyperparameters={"k": 1})
    assert a != c.make_key("x", "t", "h", "b2", 42, hyperparameters={"k": 1})
    assert a != c.make_key("x", "t", "h", "b1", 42, hyperparameters={"k": 2})
