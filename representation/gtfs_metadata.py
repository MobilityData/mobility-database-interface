

class GtfsMetadata:
    def __init__(self, md5_hash):
        """Constructor for ``GtfsMetadata``.
        :param md5_hash: The MD5 hash of the dataset version.
        """
        self.__timezone = ""
        self.__country_code = ""
        self.__sub_country_code = ""
        self.__language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__bounding_box = ""
        self.__stable_url = ""
        self.__md5_hash = md5_hash

    def __str__(self):
        """String representation of the GTFS dataset metadata.
        """
        return "Timezone: %s\n" \
               "Country code: %s\n" \
               "Sub country code: %s\n" \
               "Language code: %s\n" \
               "Start service date: %s\n" \
               "End service date: %s\n" \
               "Bounding box: %s\n" \
               "Stable url: %s\n" \
               "MD5 hash: %s" \
               % (self.__timezone,
                  self.__country_code,
                  self.__sub_country_code,
                  self.__language_code,
                  self.__start_service_date,
                  self.__end_service_date,
                  self.__bounding_box,
                  self.__stable_url,
                  self.__md5_hash)


