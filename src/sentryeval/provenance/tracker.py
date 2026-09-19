import hashlib
import json


def config_hash(config):
    return hashlib.sha256(
        json.dumps(config, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def metric_identity(provenance):
    return (provenance.dataset_version, provenance.judge_id, provenance.metric_name)
