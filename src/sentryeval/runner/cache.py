import hashlib
import json
from pathlib import Path

from diskcache import Cache

from ..core.models import Attempt


class ResultCache:
    def __init__(self, cache_dir: Path):
        self._cache = Cache(str(cache_dir))

    def make_key(
        self,
        attack_name,
        target_name,
        dataset_hash,
        behavior_id,
        seed,
        attack_params=None,
        target_params=None,
        judge_params=None,
        hyperparameters=None,
    ):
        payload = {
            "attack": attack_name,
            "target": target_name,
            "dataset_hash": dataset_hash,
            "behavior_id": behavior_id,
            "seed": seed,
            "attack_params": attack_params or {},
            "target_params": target_params or {},
            "judge_params": judge_params or {},
            "hyperparameters": hyperparameters or {},
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
        ).hexdigest()

    def get(self, key):
        raw = self._cache.get(key)
        return None if raw is None else [Attempt.model_validate(x) for x in raw]

    def set(self, key, attempts):
        self._cache.set(key, [x.model_dump(mode="json") for x in attempts])

    def invalidate(self, key):
        self._cache.delete(key)

    def clear(self):
        self._cache.clear()

    def close(self):
        self._cache.close()
