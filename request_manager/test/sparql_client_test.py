from unittest import TestCase, mock
from SPARQLWrapper import SPARQLWrapper
from request_manager.sparql_client import SparqlClient


class SparqlClientTest(TestCase):

    @mock.patch('request_manager.request_manager_containers.Configs')
    def test_sparql_client_with_none_config_should_raise_exception(self, mock_configs):
        mock_configs.config = None
        self.assertRaises(TypeError, SparqlClient, mock_configs.config)

    @mock.patch('request_manager.request_manager_containers.Configs')
    def test_sparql_client_with_empty_config_should_raise_exception(self, mock_configs):
        mock_configs.config = {}
        self.assertRaises(KeyError, SparqlClient, mock_configs.config)

    @mock.patch('request_manager.request_manager_containers.Configs')
    def test_sparql_client_with_valid_config_should_not_raise_exception(self, mock_configs):
        mock_configs.config = {"url": "http://test.com"}
        under_test = SparqlClient(mock_configs.config)
        self.assertIsInstance(under_test, SparqlClient)

    @mock.patch('request_manager.request_manager_containers.Configs')
    def test_sparql_client_session_getter_should_return_session(self, mock_configs):
        mock_configs.config = {"url": "http://test.com"}
        under_test = SparqlClient(mock_configs.config)
        self.assertIsInstance(under_test.get_service(), SPARQLWrapper)