import hashlib
import json

from ..core.exceptions import DatasetIntegrityError
from ..core.models import Behavior


def canonical_hash(records: list[dict]) -> str:
    raw = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


class BundledDataset:
    name: str
    version: str
    records: list[dict]
    sha256: str

    def load(self) -> list[Behavior]:
        actual = canonical_hash(self.records)
        if actual != self.sha256:
            raise DatasetIntegrityError(
                f"{self.name}: SHA-256 mismatch: expected {self.sha256}, got {actual}"
            )
        return [Behavior.model_validate({**r, "sha256": canonical_hash([r])}) for r in self.records]
