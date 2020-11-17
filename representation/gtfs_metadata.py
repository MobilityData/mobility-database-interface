

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
        self.__language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__bounding_box = ""
        self.__stable_url = ""

    def set_main_timezone(self, main_timezone):
        """ Set a main timezone in the GTFS metadata.
        :param main_timezone: The main timezone to set.
        """
        self.__main_timezone = main_timezone

    def set_all_timezones(self, all_timezones):
        """ Set all the timezones in the GTFS metadata.
        :param all_timezones: the list of all timezones to set.
        """
        self.__all_timezones = all_timezones

    def __str__(self):
        """String representation of the GTFS dataset metadata.
        """
        return "Main timezone: %s\n" \
               "All timezones: %s\n" \
               "Country code: %s\n" \
               "Sub country code: %s\n" \
               "Language code: %s\n" \
               "Start service date: %s\n" \
               "End service date: %s\n" \
               "Bounding box: %s\n" \
               "Stable url: %s\n" \
               "MD5 hash: %s" \
               % (self.__main_timezone,
                  ', '.join(self.__all_timezones),
                  self.__country_code,
                  self.__sub_country_code,
                  self.__language_code,
                  self.__start_service_date,
                  self.__end_service_date,
                  self.__bounding_box,
                  self.__stable_url,
                  self.__md5_hash)


