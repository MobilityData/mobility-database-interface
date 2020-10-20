import unittest
from request_manager.sparql_request_manager import SparqlRequestManager


class SparqlRequestManagerTest(unittest.TestCase):

    def test_none_response_for_request_with_none_query(self):
        query = None

        under_test = SparqlRequestManager()
        self.assertIsNone(under_test.get_response(query))

    def test_response_with_3_items_per_result_for_request_with_no_query_item_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a 
                   ?b
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a', 'b', 'c'])

    def test_response_with_b_and_c_items_per_result_for_request_with_existent_query_item_a_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   ?b
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['b', 'c'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_empty_result_for_request_with_non_existent_query_item_a_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/non-existent>
                   ?b
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['b', 'c'])
        self.assertEqual(response['results']['bindings'], [])

    def test_response_with_a_and_c_items_per_result_with_request_with_existent_query_item_b_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/P27>
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a', 'c'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_empty_result_for_request_with_non_existent_query_item_b_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/non-existent>
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a', 'c'])
        self.assertEqual(response['results']['bindings'], [])

    def test_response_with_a_and_b_items_per_result_for_request_with_existent_query_item_c_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   ?b
                   <http://wikibase.svc/entity/Q61>
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a', 'b'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_empty_result_for_request_with_non_existent_query_item_c_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   ?b
                   <http://wikibase.svc/entity/non-existent>
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a', 'b'])
        self.assertEqual(response['results']['bindings'], [])

    def test_response_with_c_item_per_result_for_request_with_existent_query_items_a_and_b_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   <http://wikibase.svc/prop/statement/P27>
                   ?c
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['c'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_b_item_per_result_for_request_with_existent_query_items_a_and_c_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   ?b
                   <http://wikibase.svc/entity/Q61>
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['b'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_a_item_per_result_for_request_with_existent_query_items_b_and_c_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/P27>
                   <http://wikibase.svc/entity/Q61>
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], ['a'])
        self.assertNotEqual(response['results']['bindings'], [])

    def test_response_with_no_result_for_request_with_3_existent_query_items_specified(self):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   <http://wikibase.svc/prop/statement/P27>
                   <http://wikibase.svc/entity/Q61>
                }"""

        under_test = SparqlRequestManager()
        response = under_test.get_response(query)
        self.assertEqual(list(response.keys())[0], 'head')
        self.assertEqual(response['head']['vars'], [])
        self.assertEqual(response['results']['bindings'], [{}])
