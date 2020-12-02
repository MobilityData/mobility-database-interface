

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
        self.__main_language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__bounding_box = ""
        self.__stable_url = ""

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

    def __str__(self):
        """String representation of the GTFS dataset metadata.
        """
        return "Timezone: %s\n" \
               "Country code: %s\n" \
               "Sub country code: %s\n" \
               "Main language code: %s\n" \
               "Start service date: %s\n" \
               "End service date: %s\n" \
               "Bounding box: %s\n" \
               "Stable url: %s\n" \
               "MD5 hash: %s" \
               % (self.__timezone,
                  self.__country_code,
                  self.__sub_country_code,
                  self.__main_language_code,
                  self.__start_service_date,
                  self.__end_service_date,
                  self.__bounding_box,
                  self.__stable_url,
                  self.__md5_hash)
