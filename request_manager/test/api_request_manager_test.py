from unittest import TestCase, mock
from requests import exceptions
from request_manager.api_request_manager import ApiRequestManager


class ApiRequestManagerTest(TestCase):
    def test_api_request_manager_initialized_with_none_api_client_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, ApiRequestManager, None)

    @mock.patch("request_manager.api_client.ApiClient")
    def test_api_request_manager_initialized_with_api_client_should_not_raise_exception(
        self, mock_api_client
    ):
        under_test = ApiRequestManager(mock_api_client)

        self.assertIsInstance(under_test, ApiRequestManager)
        mock_api_client.assert_not_called()

    @mock.patch("request_manager.api_client.ApiClient")
    def test_api_get_request_with_none_params_should_return_none(self, mock_api_client):
        params = None

        under_test = ApiRequestManager(mock_api_client)

        self.assertIsNone(under_test.execute_get(params))
        mock_api_client.assert_not_called()

    @mock.patch("request_manager.api_client.ApiClient")
    def test_api_get_request_with_none_session_should_raise_exception(
        self, mock_api_client
    ):
        params = {
            "action": "test-action",
            "ids": "test",
            "languages": "en",
            "format": "json",
        }

        mock_api_client.get_session.return_value = None
        mock_api_client.get_url.return_value = "http://test.com"
        under_test = ApiRequestManager(mock_api_client)

        self.assertRaises(AttributeError, under_test.execute_get, params)
        mock_api_client.get_session.assert_called_once()
        mock_api_client.get_url.assert_called_once()

    @mock.patch("request_manager.api_client.ApiClient")
    @mock.patch("requests.Session")
    def test_api_get_request_with_none_URL_should_return_none(
        self, mock_api_client, mock_session
    ):
        params = {
            "action": "test-action",
            "ids": "test",
            "languages": "en",
            "format": "json",
        }

        mock_session.get.side_effect = exceptions.MissingSchema
        mock_api_client.get_session.return_value = mock_session
        mock_api_client.get_url.return_value = None
        under_test = ApiRequestManager(mock_api_client)

        self.assertRaises(exceptions.MissingSchema, under_test.execute_get, params)
        mock_api_client.get_session.assert_called_once()
        mock_api_client.get_url.assert_called_once()
        mock_session.get.assert_called_once()

    @mock.patch("request_manager.api_client.ApiClient")
    @mock.patch("requests.Session")
    @mock.patch("requests.Response")
    def test_api_get_request_with_params_session_and_url_should_return_response(
        self, mock_api_client, mock_session, mock_response
    ):
        params = {
            "action": "test-action",
            "ids": "test",
            "languages": "en",
            "format": "json",
        }

        mock_response.json.return_value = "test_response"
        mock_session.get.return_value = mock_response
        mock_api_client.get_session.return_value = mock_session
        mock_api_client.get_url.return_value = "http://test.com"
        under_test = ApiRequestManager(mock_api_client)

        self.assertEqual(under_test.execute_get(params), "test_response")
        mock_api_client.get_session.assert_called_once()
        mock_api_client.get_url.assert_called_once()
        mock_session.get.assert_called_once()
        mock_response.json.assert_called_once()
