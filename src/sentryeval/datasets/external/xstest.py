from ...core.exceptions import DatasetIntegrityError


class ExternalDataset:
    def __init__(self, url, sha256):
        self.url = url
        self.sha256 = sha256

    def load(self):
        raise DatasetIntegrityError(
            "External datasets require an explicit, hash-pinned download step"
        )
