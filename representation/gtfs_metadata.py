class GtfsMetadata:
    def __init__(self, md5_hash, source_name, download_date):
        """Constructor for ``GtfsMetadata``.
        :param md5_hash: The MD5 hash of the dataset version.
        :param source_name: The name of the source of the dataset.
        :param download_date: The date when the dataset version was downloaded.
        """
        if not isinstance(md5_hash, str):
            raise TypeError("MD5 hash must be a valid MD5 hash string.")
        if not isinstance(source_name, str):
            raise TypeError("Source name must be a valid source name string.")
        if not isinstance(download_date, str):
            raise TypeError("Download date must be a valid date string.")
        self.md5_hash = md5_hash
        self.dataset_version_name = self.create_dataset_version_name(
            source_name, download_date, md5_hash
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
        if source_name.find("source") != -1:
            # Find left index of "source", minus 1 for the preceding space
            left_index = source_name.find("source") - 1
            # Compute right index from left index, plus 1 to balance the space previously considered
            right_index = left_index + len("source") + 1
            dataset_name = source_name[:left_index] + source_name[right_index:]
        else:
            dataset_name = source_name

        # Select a substring from the MD5 hash create unique identifier for the dataset name
        shorten_md5_hash = md5_hash[:6]

        # Create the full dataset version name
        dataset_version_name = "%s's %s dataset #%s" % (
            download_date,
            dataset_name,
            shorten_md5_hash,
        )

        return dataset_version_name

    def get_md5_hash(self):
        """Get the MD5 hash in the GTFS metadata.
        :return: The MD5 hash to get.
        """
        return self.md5_hash

    def get_dataset_version_name(self):
        """Get the dataset version name in the GTFS metadata.
        :return: The dataset version name to get.
        """
        return self.dataset_version_name

    def set_start_service_date(self, start_service_date):
        """Set a start service date in the GTFS metadata.
        :param start_service_date: The start_service_date to set.
        """
        self.start_service_date = start_service_date

    def get_start_service_date(self):
        """Get the start service date in the GTFS metadata.
        :return: The start_service_date to get.
        """
        return self.start_service_date

    def set_end_service_date(self, end_service_date):
        """Set a end service date in the GTFS metadata.
        :param end_service_date: The end service date to set.
        """
        self.end_service_date = end_service_date

    def get_end_service_date(self):
        """Get the end service date in the GTFS metadata.
        :return: The end_service_date to get.
        """
        return self.end_service_date

    def set_start_timestamp(self, start_timestamp):
        """Set a start timestamp in the GTFS metadata.
        :param start_timestamp: The start timestamp to set.
        """
        self.start_timestamp = start_timestamp

    def get_start_timestamp(self):
        """Get the start timestamp in the GTFS metadata.
        :return: The start_timestamp to get.
        """
        return self.start_timestamp

    def set_end_timestamp(self, end_timestamp):
        """Set a end timestamp in the GTFS metadata.
        :param end_timestamp: The end timestamp to set.
        """
        self.end_timestamp = end_timestamp

    def get_end_timestamp(self):
        """Get the end timestamp in the GTFS metadata.
        :return: The end_timestamp to get.
        """
        return self.end_timestamp

    def set_main_language_code(self, main_language_code):
        """Set a main language code in the GTFS metadata.
        :param main_language_code: The main language code to set.
        """
        self.main_language_code = main_language_code

    def get_main_language_code(self):
        """Get the main language code in the GTFS metadata.
        :return: The main language code to get.
        """
        return self.main_language_code

    def set_main_timezone(self, main_timezone):
        """Set a main timezone in the GTFS metadata.
        :param main_timezone: The main timezone to set.
        """
        self.main_timezone = main_timezone

    def get_main_timezone(self):
        """Get the main timezone in the GTFS metadata.
        :return: The main timezone to get.
        """
        return self.main_timezone

    def set_all_timezones(self, all_timezones):
        """Set all the timezones in the GTFS metadata.
        :param all_timezones: the list of all timezones to set.
        """
        self.all_timezones = all_timezones

    def get_all_timezones(self):
        """Get all the timezones in the GTFS metadata.
        :return: the list of all timezones to get.
        """
        return self.all_timezones

    def set_bounding_box(self, bounding_box):
        """Set the geographical bounding box in the GTFS metadata.
        :param bounding_box: the bounding box to set.
        """
        self.bounding_box = bounding_box

    def get_bounding_box(self):
        """Get the geographical bounding box in the GTFS metadata.
        :return: the bounding box to get.
        """
        return self.bounding_box

    def set_bounding_octagon(self, bounding_octagon):
        """Set the geographical bounding octagon in the GTFS metadata.
        :param bounding_octagon: the bounding octagon to set.
        """
        self.bounding_octagon = bounding_octagon

    def get_bounding_octagon(self):
        """Get the geographical bounding octagon in the GTFS metadata.
        :return: the bounding octagon to get.
        """
        return self.bounding_octagon

    def set_agencies_count(self, agencies_count):
        """Set the agencies count in the GTFS metadata.
        :param agencies_count: the agencies count to set.
        """
        self.agencies_count = agencies_count

    def get_agencies_count(self):
        """Get the agencies count in the GTFS metadata.
        :return: the agencies count to set.
        """
        return self.agencies_count

    def set_routes_count_by_type(self, routes_count_by_type):
        """Set the routes count by type in the GTFS metadata.
        :param routes_count_by_type: the routes count by type to set.
        """
        self.routes_count_by_type = routes_count_by_type

    def get_routes_count_by_type(self):
        """Get the routes count by type in the GTFS metadata.
        :return: the routes count by type to set.
        """
        return self.routes_count_by_type

    def set_stops_count_by_type(self, stops_count_by_type):
        """Set the stops count by type in the GTFS metadata.
        :param stops_count_by_type: the stops count by type to set.
        """
        self.stops_count_by_type = stops_count_by_type

    def get_stops_count_by_type(self):
        """Get the stops count by type in the GTFS metadata.
        :return: the stops count by type to set.
        """
        return self.stops_count_by_type

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
