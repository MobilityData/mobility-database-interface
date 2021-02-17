import sys
from SPARQLWrapper import SPARQLWrapper


class SparqlClient:
    def __init__(self, config):
        """Constructor for ``SparqlClient``."""
        self.__service = None
        try:
            self.__url = config["url"]
        except Exception as e:
            raise e

    def __get_service(self):
        """Private getter for the wrapper service of the SPARQL client. Initialize the service if set at none.
        :return: The wrapper service of the SPARQL client.
        """
        if self.__service is None:
            user_agent = "WDQS-example Python/%s.%s" % (
                sys.version_info[0],
                sys.version_info[1],
            )
            self.__service = SPARQLWrapper(self.__url, agent=user_agent)
        return self.__service

    def get_service(self):
        """Public getter for the wrapper service of the SPARQL client.
        :return: The wrapper service of the SPARQL client.
        """
        return self.__get_service()
