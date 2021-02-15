class GtfsMetadata:
    def __init__(self, md5_hash):
        """Constructor for ``GtfsMetadata``.
        :param md5_hash: The MD5 hash of the dataset version.
        """
        if md5_hash is None or not isinstance(md5_hash, str):
            raise TypeError("MD5 hash must be a valid MD5 hash string.")
        self.md5_hash = md5_hash
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

    def __str__(self):
        """String representation of the GTFS dataset metadata."""
        return (
            "Main timezone: %s\n"
            "All timezones: %s\n"
            "Country code: %s\n"
            "Sub country code: %s\n"
            "Main language code: %s\n"
            "Start service date: %s\n"
            "End service date: %s\n"
            "Start timestamp: %s\n"
            "End timestamp: %s\n"
            "Bounding box: %s\n"
            "Bounding octagon: %s\n"
            "Agencies count: %s\n"
            "Routes count by type: %s\n"
            "Stops count by type: %s\n"
            "Stable url: %s\n"
            "MD5 hash: %s"
            % (
                self.main_timezone,
                ", ".join(self.all_timezones),
                self.country_code,
                self.sub_country_code,
                self.main_language_code,
                self.start_service_date,
                self.end_service_date,
                self.start_timestamp,
                self.end_timestamp,
                self.bounding_box,
                self.bounding_octagon,
                self.agencies_count,
                self.routes_count_by_type,
                self.stops_count_by_type,
                self.stable_url,
                self.md5_hash,
            )
        )
