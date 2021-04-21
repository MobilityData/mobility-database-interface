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
