

class ApiRequestManager:

    def __init__(self, client):
        """Constructor for ``ApiRequestManager``.
        """
        try:
            self._api_client = client
        except Exception as e:
            raise e

    def execute_get(self, params):
        """Execute GET request with the API client.
        :param params: The params for the request to make to the API client.
        :return: The response returned by the API client.
        """
        if params is not None:
            return self._api_client.get(params)
