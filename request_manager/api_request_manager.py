import requests
from utilities import external_utils


class ApiRequestManager:

    def __init__(self):
        """Constructor for ``ApiRequestManager``.
        """
        self.session = None
        self.url = external_utils.get_db_api_url()

    def __get_session(self):
        """Get the session for the API. Initialize the session if set at none.
        :return: The session for the API.
        """
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def get_response(self, params):
        """Get a response for a query made to the API of the database.
        :param params: The params for the query to make to the API.
        :return: The response returned by the API.
        """
        if params is not None:
            session = self.__get_session()
            return session.get(url=self.url, params=params).json()
