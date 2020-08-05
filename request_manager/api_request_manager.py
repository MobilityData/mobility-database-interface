import requests


class ApiRequestManager:

    def __init__(self):
        self.session = None
        self.url = 'http://staging.mobilitydatabase.org/w/api.php'

    def __get_session(self):
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def get_request(self, params):
        session = self.__get_session()
        return session.get(url=self.url, params=params)
