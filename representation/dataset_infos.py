class DatasetInfos:
    def __init__(self):
        """Constructor for ``DatasetInfos``."""
        self.source_name = ""
        self.entity_code = ""
        self.url = ""
        self.zip_path = ""
        self.download_date = ""
        self.sha1_hash = ""
        self.previous_sha1_hashes = set()
        self.previous_versions = set()

    def __str__(self):
        return (
            f"Source name: {self.source_name}\n"
            f"Entity code: {self.entity_code}\n"
            f"URL: {self.url}\n"
            f"Zip path: {self.zip_path}\n"
            f"Download date: {self.download_date}\n"
            f"SHA-1 hash: {self.sha1_hash}\n"
            f"Previous SHA-1 hashes: {self.previous_sha1_hashes}\n"
            f"Previous versions: {self.previous_versions}\n"
        )
