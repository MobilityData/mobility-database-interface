import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from utilities import external_utils


class SparqlRequestManager:

    def __init__(self):
        self.sparql_service = None
        self.url = external_utils.get_db_query_service_url()

    def __get_sparql_service(self):
        if self.sparql_service is None:
            user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
            self.sparql_service = SPARQLWrapper(self.url, agent=user_agent)
        return self.sparql_service

    def get_response(self, query):
        sparql = self.__get_sparql_service()
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()