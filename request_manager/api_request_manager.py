import requests
from utilities import external_utils


class ApiRequestManager:

    def __init__(self):
        self.session = None
        self.url = external_utils.get_db_api_url()

    def __get_session(self):
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def get_response(self, params):
        if params is not None:
            session = self.__get_session()
            return session.get(url=self.url, params=params).json()
