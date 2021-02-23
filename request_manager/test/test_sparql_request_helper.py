from unittest import TestCase, mock
from request_manager.sparql_request_helper import sparql_request
from utilities.constants import STAGING_SPARQL_URL


class TestSparqlRequestManager(TestCase):
    def test_sparql_get_request_with_none_api_url_should_raise_exception(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a 
                   ?b
                   ?c
                }"""

        self.assertRaises(TypeError, sparql_request, None, query)

    def test_sparql_get_request_non_str_query(self):
        query = 132314

        self.assertRaises(Exception, sparql_request, STAGING_SPARQL_URL, query)

    def test_sparql_get_request_query_empty_str(self):
        query = ""

        self.assertRaises(Exception, sparql_request, STAGING_SPARQL_URL, query)
