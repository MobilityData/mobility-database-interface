from unittest import TestCase, mock
from request_manager.sparql_request_manager import SparqlRequestManager


class SparqlRequestManagerTest(TestCase):

    def test_sparql_request_manager_initialized_with_none_sparql_client_should_raise_exception(self):
        self.assertRaises(TypeError, SparqlRequestManager, None)

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_sparql_request_manager_initialized_with_sparql_client_should_not_raise_exception(self, mock_sparql_client):
        under_test = SparqlRequestManager(mock_sparql_client)

        self.assertIsInstance(under_test, SparqlRequestManager)
        mock_sparql_client.assert_not_called()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_sparql_get_request_with_none_query_should_return_none(self, mock_sparql_client):
        query = None

        under_test = SparqlRequestManager(mock_sparql_client)

        self.assertIsNone(under_test.execute_get(query))
        mock_sparql_client.assert_not_called()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    def test_sparql_get_request_with_none_service_should_raise_exception(self, mock_sparql_client):
        query = """
                SELECT *
                WHERE 
                {
                   ?a 
                   ?b
                   ?c
                }"""

        mock_sparql_client.get_service.return_value = None
        under_test = SparqlRequestManager(mock_sparql_client)

        self.assertRaises(AttributeError, under_test.execute_get, query)
        mock_sparql_client.get_service.assert_called_once()

    @mock.patch('request_manager.sparql_client.SparqlClient')
    @mock.patch('SPARQLWrapper.SPARQLWrapper')
    @mock.patch('SPARQLWrapper.Wrapper.QueryResult')
    def test_sparql_get_request_with_query_and_session_should_return_response(self, mock_sparql_client,
                                                                            mock_service, mock_response):
        query = """
                SELECT *
                WHERE 
                {
                   ?a 
                   ?b
                   ?c
                }"""

        mock_response.convert.return_value = "test_response"
        mock_service.query.return_value = mock_response
        mock_sparql_client.get_service.return_value = mock_service
        under_test = SparqlRequestManager(mock_sparql_client)

        self.assertEqual(under_test.execute_get(query), "test_response")
        mock_sparql_client.get_service.assert_called_once()
        mock_service.query.assert_called_once()
        mock_response.convert.assert_called_once()
