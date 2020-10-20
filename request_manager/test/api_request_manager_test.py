from unittest import TestCase, mock
import warnings
from request_manager.api_request_manager import ApiRequestManager


def ignore_resource_warnings(test_func):
    """Removes the resource warning raised by testing sessions without closing them (normal class behaviour).
    """
    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return test


class ApiRequestManagerTest(TestCase):

    @mock.patch('request_manager.api_client.ApiClient')
    def test_none_response_for_request_with_none_params(self, mock_api_client):
        params = None

        under_test = ApiRequestManager(mock_api_client)
        self.assertIsNone(under_test.execute_get(params))
        mock_api_client.assert_not_called()

    @ignore_resource_warnings
    @mock.patch('request_manager.api_client.ApiClient')
    def test_error_response_for_request_with_non_existent_entity(self, mock_api_client):
        params = {
            "action": "wbgetentities",
            "ids": "non_existent",
            "languages": "en",
            "format": "json"
        }
        mock_api_client.get.return_value = 'testing'

        under_test = ApiRequestManager(mock_api_client)
        response = under_test.execute_get(params)
        self.assertEqual(response, 'testing')
        mock_api_client.get.assert_called_once()

    @ignore_resource_warnings
    @mock.patch('request_manager.api_client.ApiClient')
    def test_error_response_for_request_with_non_existent_action(self, mock_api_client):
        params = {
            "action": "non_existent",
            "ids": "Q66",
            "languages": "en",
            "format": "json"
        }
        mock_api_client.get.return_value = 'testing'

        under_test = ApiRequestManager(mock_api_client)
        response = under_test.execute_get(params)
        self.assertEqual(response, 'testing')
        mock_api_client.get.assert_called_once()

    @ignore_resource_warnings
    @mock.patch('request_manager.api_client.ApiClient')
    def test_warning_response_for_request_with_non_existent_language(self, mock_api_client):
        params = {
            "action": "wbgetentities",
            "ids": "Q66",
            "languages": "non_existent",
            "format": "json"
        }
        mock_api_client.get.return_value = 'testing'

        under_test = ApiRequestManager(mock_api_client)
        response = under_test.execute_get(params)
        self.assertEqual(response, 'testing')
        mock_api_client.get.assert_called_once()

    @ignore_resource_warnings
    @mock.patch('request_manager.api_client.ApiClient')
    def test_normal_response_for_request_with_existent_params(self, mock_api_client):
        params = {
            "action": "wbgetentities",
            "ids": "Q66",
            "languages": "en",
            "format": "json"
        }
        mock_api_client.get.return_value = 'testing'

        under_test = ApiRequestManager(mock_api_client)
        response = under_test.execute_get(params)
        self.assertEqual(response, 'testing')
        mock_api_client.get.assert_called_once()
