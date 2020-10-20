import sys
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlClient:

    def __init__(self, config):
        """Constructor for ``SparqlClient``.
        """
        self.service = None
        self.config = config

    def __get_service(self):
        """Get the wrapper service for the SPARQL client. Initialize the service if set at none.
        :return: The wrapper service for the SPARQL client.
        """
        if self.service is None:
            url = self.config.get('url')
            user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
            self.service = SPARQLWrapper(url, agent=user_agent)
        return self.service

    def get(self, query):
        """Get a response for a query made to the SPARQL service of the database.
        :param query: The query to make to the SPARQL service.
        :return: The response returned by the SPARQL service.
        """
        service = self.__get_service()
        service.setQuery(query)
        service.setReturnFormat(JSON)
        return service.query().convert()

