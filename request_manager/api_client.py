import requests


class ApiClient:

    def __init__(self, config):
        """Constructor for ``ApiClient``.
        """
        self.__session = None
        try:
            self.__url = config['url']
        except Exception as e:
            raise e

    def __get_session(self):
        """Private getter for the session of the API client. Initialize the session if set at none.
        :return: The session of the API client.
        """
        if self.__session is None:
            self.__session = requests.Session()
        return self.__session

    def get_session(self):
        """Public getter for the session of the API client.
        :return: The session of the API client.
        """
        return self.__get_session()

    def get_url(self):
        """Getter for the URL of the API client.
        :return: The URL of the API client.
        """
        return self.__url

