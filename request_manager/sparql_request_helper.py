import sys

from SPARQLWrapper import SPARQLWrapper, JSON

from utilities.constants import STAGING_SPARQL_URL, PRODUCTION_SPARQL_URL

SPARQL_USER_AGENT = f"WDQS-example Python/{sys.version_info[0]}.{sys.version_info[1]}"


def sparql_request(sparql_api, query):
    if sparql_api not in [PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL]:
        raise TypeError(
            f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}"
        )
    if not isinstance(query, str) or len(query) == 0:
        raise Exception("query should not be empty ")

    service = SPARQLWrapper(sparql_api, agent=SPARQL_USER_AGENT)
    service.setQuery(query)
    service.setReturnFormat(JSON)
    response = service.query().convert()
    return response
