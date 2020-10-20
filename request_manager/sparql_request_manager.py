

class SparqlRequestManager:

    def __init__(self, client):
        """Constructor for ``SparqlRequestManager``.
        """
        try:
            self._sparql_client = client
        except Exception as e:
            raise e

    def execute_get(self, query):
        """Get a response for a query made to the SPARQL service of the database.
        :param query: The query to make to the SPARQL service.
        :return: The response returned by the SPARQL service.
        """
        if query is not None:
            return self._sparql_client.get(query)
