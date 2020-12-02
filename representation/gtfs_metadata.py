

class GtfsMetadata:
    def __init__(self, md5_hash):
        """Constructor for ``GtfsMetadata``.
        :param md5_hash: The MD5 hash of the dataset version.
        """
        if md5_hash is None or not isinstance(md5_hash, str):
            raise TypeError('MD5 hash must be a valid MD5 hash string.')
        self.__md5_hash = md5_hash
        self.__timezone = ""
        self.__country_code = ""
        self.__sub_country_code = ""
        self.__language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__start_timestamp = ""
        self.__end_timestamp = ""
        self.__bounding_box = ""
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

    def __str__(self):
        """String representation of the GTFS dataset metadata.
        """
        return "Timezone: %s\n" \
               "Country code: %s\n" \
               "Sub country code: %s\n" \
               "Language code: %s\n" \
               "Start service date: %s\n" \
               "End service date: %s\n" \
               "Start timestamp: %s\n" \
               "End timestamp: %s\n" \
               "Bounding box: %s\n" \
               "Stable url: %s\n" \
               "MD5 hash: %s" \
               % (self.__timezone,
                  self.__country_code,
                  self.__sub_country_code,
                  self.__language_code,
                  self.__start_service_date,
                  self.__end_service_date,
                  self.__start_timestamp,
                  self.__end_timestamp,
                  self.__bounding_box,
                  self.__stable_url,
                  self.__md5_hash)


