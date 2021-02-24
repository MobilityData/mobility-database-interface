from representation.dataset_infos import DatasetInfos

SOURCE = "source"
SHORTEN_MD5_HASH_LEN = 6


class GtfsMetadata:
    def __init__(self, dataset_infos):
        """Constructor for ``GtfsMetadata``.
        :param dataset_infos: The processing infos of the dataset.
        """
        if not isinstance(dataset_infos, DatasetInfos):
            raise TypeError("Dataset infos must be a valid DatasetInfos.")

        self.source_entity_code = dataset_infos.entity_code
        self.md5_hash = dataset_infos.md5_hash
        self.dataset_version_name = self.create_dataset_version_name(
            dataset_infos.source_name,
            dataset_infos.download_date,
            dataset_infos.md5_hash,
        )
        self.main_timezone = ""
        self.all_timezones = []
        self.country_code = ""
        self.sub_country_code = ""
        self.main_language_code = ""
        self.start_service_date = ""
        self.end_service_date = ""
        self.start_timestamp = ""
        self.end_timestamp = ""
        self.bounding_box = {}
        self.bounding_octagon = {}
        self.agencies_count = 0
        self.routes_count_by_type = {}
        self.stops_count_by_type = {}
        self.stable_url = ""

    def create_dataset_version_name(self, source_name, download_date, md5_hash):
        """Create the dataset version name from the source name, download date and MD5 hash.
        :param md5_hash: The MD5 hash of the dataset version.
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

        # Select a substring from the MD5 hash create unique identifier for the dataset name
        shorten_md5_hash = md5_hash[:SHORTEN_MD5_HASH_LEN]

        # Create the full dataset version name
        dataset_version_name = (
            f"{download_date}'s {dataset_name} dataset #{shorten_md5_hash}"
        )

        return dataset_version_name

    def __str__(self):
        """String representation of the GTFS dataset metadata."""
        return (
            f"Dataset version name: {self.dataset_version_name}\n"
            f"Main timezone: {self.main_timezone}\n"
            f"All timezones: {', '.join(self.all_timezones)}\n"
            f"Country code: {self.country_code}\n"
            f"Sub country code: {self.sub_country_code}\n"
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
            f"MD5 hash: {self.md5_hash}"
        )
