class ApiRequestManager:
    def __init__(self, client):
        """Constructor for ``ApiRequestManager``."""
        try:
            if client is None:
                raise TypeError("Client must be a valid ApiClient.")
            self.__api_client = client
        except Exception as e:
            raise e

    def execute_get(self, params):
        """Execute GET request with the API client.
        :param params: The params for the request to make to the API client.
        :return: The response returned by the API client.
        """
        if params is not None:
            try:
                session = self.__api_client.get_session()
                url = self.__api_client.get_url()
                response = session.get(url=url, params=params).json()
            except Exception as e:
                raise e
            else:
                return response
