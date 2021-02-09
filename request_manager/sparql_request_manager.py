from SPARQLWrapper import JSON


class SparqlRequestManager:
    def __init__(self, client):
        """Constructor for ``SparqlRequestManager``."""
        try:
            if client is None:
                raise TypeError("Client must be a valid ApiClient.")
            self.__sparql_client = client
        except Exception as e:
            raise e

    def execute_get(self, query):
        """Get a response for a query made to the SPARQL service of the database.
        :param query: The query to make to the SPARQL service.
        :return: The response returned by the SPARQL service.
        """
        if query is not None:
            try:
                service = self.__sparql_client.get_service()
                service.setQuery(query)
                service.setReturnFormat(JSON)
                response = service.query().convert()
            except Exception as e:
                raise e
            else:
                return response
