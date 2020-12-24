

class GtfsMetadata:
    def __init__(self, md5_hash):
        """Constructor for ``GtfsMetadata``.
        :param md5_hash: The MD5 hash of the dataset version.
        """
        if md5_hash is None or not isinstance(md5_hash, str):
            raise TypeError('MD5 hash must be a valid MD5 hash string.')
        self.__md5_hash = md5_hash
        self.__main_timezone = ""
        self.__all_timezones = []
        self.__country_code = ""
        self.__sub_country_code = ""
        self.__main_language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__start_timestamp = ""
        self.__end_timestamp = ""
        self.__bounding_box = ""
        self.__agencies_count = 0
        self.__routes_count_by_type = {}
        self.__stops_count_by_type = {}
        self.__stable_url = ""

    def set_start_service_date(self, start_service_date):
        """ Set a start service date in the GTFS metadata.
        :param start_service_date: The start_service_date to set.
        """
        self.__start_service_date = start_service_date

    def get_start_service_date(self):
        """ Get the start service date in the GTFS metadata.
        :return: The start_service_date to set.
        """
        return self.__start_service_date

    def set_end_service_date(self, end_service_date):
        """ Set a end service date in the GTFS metadata.
        :param end_service_date: The end service date to set.
        """
        self.__end_service_date = end_service_date

    def get_end_service_date(self):
        """ Get the end service date in the GTFS metadata.
        :return: The end_service_date to set.
        """
        return self.__end_service_date

    def set_start_timestamp(self, start_timestamp):
        """ Set a start timestamp in the GTFS metadata.
        :param start_timestamp: The start timestamp to set.
        """
        self.__start_timestamp = start_timestamp

    def get_start_timestamp(self):
        """ Get the start timestamp in the GTFS metadata.
        :return: The start_timestamp to set.
        """
        return self.__start_timestamp

    def set_end_timestamp(self, end_timestamp):
        """ Set a end timestamp in the GTFS metadata.
        :param end_timestamp: The end timestamp to set.
        """
        self.__end_timestamp = end_timestamp

    def get_end_timestamp(self):
        """ Get the end timestamp in the GTFS metadata.
        :return: The end_timestamp to set.
        """
        return self.__end_timestamp

    def set_main_language_code(self, main_language_code):
        """ Set a main language code in the GTFS metadata.
        :param main_language_code: The main language code to set.
        """
        self.__main_language_code = main_language_code

    def get_main_language_code(self):
        """ Get the main language code in the GTFS metadata.
        :return: The main language code to set.
        """
        return self.__main_language_code

    def set_main_timezone(self, main_timezone):
        """ Set a main timezone in the GTFS metadata.
        :param main_timezone: The main timezone to set.
        """
        self.__main_timezone = main_timezone

    def get_main_timezone(self):
        """ Get the main timezone in the GTFS metadata.
        :return: The main timezone to set.
        """
        return self.__main_timezone

    def set_all_timezones(self, all_timezones):
        """ Set all the timezones in the GTFS metadata.
        :param all_timezones: the list of all timezones to set.
        """
        self.__all_timezones = all_timezones

    def get_all_timezones(self):
        """ Get all the timezones in the GTFS metadata.
        :return: the list of all timezones to set.
        """
        return self.__all_timezones

    def set_agencies_count(self, agencies_count):
        """ Set the agencies count in the GTFS metadata.
        :param agencies_count: the agencies count to set.
        """
        self.__agencies_count = agencies_count

    def get_agencies_count(self):
        """ Get the agencies count in the GTFS metadata.
        :return: the agencies count to set.
        """
        return self.__agencies_count

    def set_routes_count_by_type(self, routes_count_by_type):
        """ Set the routes count by type in the GTFS metadata.
        :param routes_count_by_type: the routes count by type to set.
        """
        self.__routes_count_by_type = routes_count_by_type

    def get_routes_count_by_type(self):
        """ Get the routes count by type in the GTFS metadata.
        :return: the routes count by type to set.
        """
        return self.__routes_count_by_type

    def set_stops_count_by_type(self, stops_count_by_type):
        """ Set the stops count by type in the GTFS metadata.
        :param stops_count_by_type: the stops count by type to set.
        """
        self.__stops_count_by_type = stops_count_by_type

    def get_stops_count_by_type(self):
        """ Get the stops count by type in the GTFS metadata.
        :return: the stops count by type to set.
        """
        return self.__stops_count_by_type

    def __str__(self):
        """String representation of the GTFS dataset metadata.
        """
        return "Main timezone: %s\n" \
               "All timezones: %s\n" \
               "Country code: %s\n" \
               "Sub country code: %s\n" \
               "Main language code: %s\n" \
               "Start service date: %s\n" \
               "End service date: %s\n" \
               "Start timestamp: %s\n" \
               "End timestamp: %s\n" \
               "Bounding box: %s\n" \
               "Agencies count: %s\n" \
               "Routes count by type: %s\n" \
               "Stops count by type: %s\n" \
               "Stable url: %s\n" \
               "MD5 hash: %s" \
               % (self.__main_timezone,
                  ', '.join(self.__all_timezones),
                  self.__country_code,
                  self.__sub_country_code,
                  self.__main_language_code,
                  self.__start_service_date,
                  self.__end_service_date,
                  self.__start_timestamp,
                  self.__end_timestamp,
                  self.__bounding_box,
                  self.__agencies_count,
                  self.__routes_count_by_type,
                  self.__stops_count_by_type,
                  self.__stable_url,
                  self.__md5_hash)
