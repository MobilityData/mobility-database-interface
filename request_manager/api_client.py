import requests


class ApiClient:

    def __init__(self, config):
        """Constructor for ``ApiClient``.
        """
        self.session = None
        self.config = config

    def __get_session(self):
        """Get the session for the API client. Initialize the session if set at none.
        :return: The session for the API client.
        """
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def get(self, params):
        """GET request for a request made to the API of the database.
        :param params: The params for the request to make to the API.
        :return: The response returned by the API.
        """
        session = self.__get_session()
        url = self.config.get('url')
        return session.get(url=url, params=params).json()

