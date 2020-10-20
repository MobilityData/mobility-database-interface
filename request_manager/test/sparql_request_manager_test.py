from unittest import TestCase, mock
from request_manager.sparql_request_manager import SparqlRequestManager


class SparqlRequestManagerTest(TestCase):

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_none_response_for_request_with_none_query(self, mock_sparql_client):
        query = None

        under_test = SparqlRequestManager(mock_sparql_client)
        self.assertIsNone(under_test.execute_get(query))
        mock_sparql_client.assert_not_called()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_3_items_per_result_for_request_with_no_query_item_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a 
                   ?b
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_b_and_c_items_per_result_for_request_with_existent_query_item_a_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   ?b
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_empty_result_for_request_with_non_existent_query_item_a_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/non-existent>
                   ?b
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_a_and_c_items_per_result_with_request_with_existent_query_item_b_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/P27>
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_empty_result_for_request_with_non_existent_query_item_b_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/non-existent>
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_a_and_b_items_per_result_for_request_with_existent_query_item_c_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   ?b
                   <http://wikibase.svc/entity/Q61>
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_empty_result_for_request_with_non_existent_query_item_c_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   ?b
                   <http://wikibase.svc/entity/non-existent>
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_c_item_per_result_for_request_with_existent_query_items_a_and_b_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   <http://wikibase.svc/prop/statement/P27>
                   ?c
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_b_item_per_result_for_request_with_existent_query_items_a_and_c_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   ?b
                   <http://wikibase.svc/entity/Q61>
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_a_item_per_result_for_request_with_existent_query_items_b_and_c_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a
                   <http://wikibase.svc/prop/statement/P27>
                   <http://wikibase.svc/entity/Q61>
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_response_with_no_result_for_request_with_3_existent_query_items_specified(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   <http://wikibase.svc/entity/statement/Q66-ea3ad33f-423c-6a84-1833-487a28ef5738>
                   <http://wikibase.svc/prop/statement/P27>
                   <http://wikibase.svc/entity/Q61>
                }"""
        mock_sparql_client.get.return_value = 'testing'

        under_test = SparqlRequestManager(mock_sparql_client)
        response = under_test.execute_get(query)
        self.assertEqual(response, 'testing')
        mock_sparql_client.get.assert_called_once()
