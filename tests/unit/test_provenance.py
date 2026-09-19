from sentryeval.provenance.tracker import config_hash


def test_hash_order_independent():
    assert config_hash({"a": 1, "b": 2}) == config_hash({"b": 2, "a": 1})
