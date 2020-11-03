

class GtfsMetadata:
    def __init__(self, md5_hash):
        self.__timezone = ""
        self.__country_code = ""
        self.__sub_country_code = ""
        self.__language_code = ""
        self.__start_service_date = ""
        self.__end_service_date = ""
        self.__bounding_box = ""
        self.__stable_url = ""
        self.__md5_hash = md5_hash

    def print(self):
        print("Timezone: %s" % self.__timezone)
        print("Country code: %s" % self.__country_code)
        print("Sub country code: %s" % self.__sub_country_code)
        print("Language code: %s" % self.__language_code)
        print("Start service date: %s" % self.__start_service_date)
        print("End service date: %s" % self.__end_service_date)
        print("Bounding box: %s" % self.__bounding_box)
        print("Stable url: %s" % self.__stable_url)
        print("MD5 has: %s" % self.__md5_hash)


