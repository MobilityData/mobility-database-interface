from representation.dataset_infos import DatasetInfos

SOURCE = "source"
SHORTEN_SHA1_HASH_LEN = 6


class GtfsMetadata:
    def __init__(self, dataset_infos):
        """Constructor for ``GtfsMetadata``.
        :param dataset_infos: The processing infos of the dataset.
        """
        if not isinstance(dataset_infos, DatasetInfos):
            raise TypeError("Dataset infos must be a valid DatasetInfos.")

        self.source_entity_code = dataset_infos.entity_code
        self.dataset_version_entity_code = None
        self.sha1_hash = dataset_infos.sha1_hash
        self.dataset_version_name = self.create_dataset_version_name(
            dataset_infos.source_name,
            dataset_infos.download_date,
            dataset_infos.sha1_hash,
        )
        self.main_timezone = None
        self.other_timezones = None
        self.country_codes = None
        self.main_language_code = None
        self.start_service_date = None
        self.end_service_date = None
        self.start_timestamp = None
        self.end_timestamp = None
        self.bounding_box = None
        self.bounding_octagon = None
        self.agencies_count = None
        self.routes_count_by_type = None
        self.stops_count_by_type = None
        self.stable_url = None

    def create_dataset_version_name(self, source_name, download_date, sha1_hash):
        """Create the dataset version name from the source name, download date and SHA-1 hash.
        :param sha1_hash: The SHA-1 hash of the dataset version.
        :param source_name: The name of the source of the dataset.
        :param download_date: The date when the dataset version was downloaded.
        :return: The dataset version name of the dataset version.
        """
        # Remove "source" from source name string
        if source_name.find(SOURCE) != -1:
            # Find left index of "source", minus 1 for the preceding space
            left_index = source_name.find(SOURCE) - 1
            # Compute right index from left index, plus 1 to balance the space previously considered
            right_index = left_index + len(SOURCE) + 1
            dataset_name = source_name[:left_index] + source_name[right_index:]
        else:
            dataset_name = source_name

        # Select a substring from the SHA-1 hash create unique identifier for the dataset name
        shorten_sha1_hash = sha1_hash[:SHORTEN_SHA1_HASH_LEN]

        # Create the full dataset version name
        dataset_version_name = (
            f"{download_date}'s {dataset_name} dataset #{shorten_sha1_hash}"
        )

        return dataset_version_name

    def __str__(self):
        """String representation of the GTFS dataset metadata."""
        return (
            f"Dataset version name: {self.dataset_version_name}\n"
            f"Main timezone: {self.main_timezone}\n"
            f"Other timezones: {self.other_timezones}\n"
            f"Country codes: {self.country_codes}\n"
            f"Main language code: {self.main_language_code}\n"
            f"Start service date: {self.start_service_date}\n"
            f"End service date: {self.end_service_date}\n"
            f"Start timestamp: {self.start_timestamp}\n"
            f"End timestamp: {self.end_timestamp}\n"
            f"Bounding box: {self.bounding_box}\n"
            f"Bounding octagon: {self.bounding_octagon}\n"
            f"Agencies count: {self.agencies_count}\n"
            f"Routes count by type: {self.routes_count_by_type}\n"
            f"Stops count by type: {self.stops_count_by_type}\n"
            f"Stable url: {self.stable_url}\n"
            f"SHA-1 hash: {self.sha1_hash}"
        )
