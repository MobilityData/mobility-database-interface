from unittest import TestCase, mock
from requests import Session
from request_manager.api_client import ApiClient


class ApiClientTest(TestCase):
    @mock.patch("request_manager.request_manager_containers.Configs")
    def test_api_client_with_none_config_should_raise_exception(self, mock_configs):
        mock_configs.config = None
        self.assertRaises(TypeError, ApiClient, mock_configs.config)

    @mock.patch("request_manager.request_manager_containers.Configs")
    def test_api_client_with_empty_config_should_raise_exception(self, mock_configs):
        mock_configs.config = {}
        self.assertRaises(KeyError, ApiClient, mock_configs.config)

    @mock.patch("request_manager.request_manager_containers.Configs")
    def test_api_client_with_valid_config_should_not_raise_exception(
        self, mock_configs
    ):
        mock_configs.config = {"url": "http://test.com"}
        under_test = ApiClient(mock_configs.config)
        self.assertIsInstance(under_test, ApiClient)

    @mock.patch("request_manager.request_manager_containers.Configs")
    def test_api_client_session_getter_should_return_session(self, mock_configs):
        mock_configs.config = {"url": "http://test.com"}
        under_test = ApiClient(mock_configs.config)
        self.assertIsInstance(under_test.get_session(), Session)

    @mock.patch("request_manager.request_manager_containers.Configs")
    def test_api_client_url_getter_should_return_url(self, mock_configs):
        mock_configs.config = {"url": "http://test.com"}
        under_test = ApiClient(mock_configs.config)
        self.assertEqual(under_test.get_url(), "http://test.com")
