import unittest
import warnings
from request_manager.api_request_manager import ApiRequestManager


def ignore_resource_warnings(test_func):
    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return test


class ApiRequestManagerTest(unittest.TestCase):

    def test_request_with_none_params_should_return_none(self):
        params = None

        under_test = ApiRequestManager()
        self.assertIsNone(under_test.get_response(params))

    @ignore_resource_warnings
    def test_request_with_non_existent_entity_should_return_error(self):
        params = {
            "action": "wbgetentities",
            "ids": "non_existent",
            "languages": "en",
            "format": "json"
        }

        under_test = ApiRequestManager()
        response = under_test.get_response(params)
        self.assertEqual(list(response.keys()), ['error'])
        self.assertEqual(response['error']['code'], 'no-such-entity')

    @ignore_resource_warnings
    def test_request_with_non_existent_action_should_return_error(self):
        params = {
            "action": "non_existent",
            "ids": "Q66",
            "languages": "en",
            "format": "json"
        }

        under_test = ApiRequestManager()
        response = under_test.get_response(params)
        self.assertEqual(list(response.keys()), ['error'])
        self.assertEqual(response['error']['code'], 'unknown_action')

    @ignore_resource_warnings
    def test_request_with_non_existent_language_should_return_warning(self):
        params = {
            "action": "wbgetentities",
            "ids": "Q66",
            "languages": "non_existent",
            "format": "json"
        }

        under_test = ApiRequestManager()
        response = under_test.get_response(params)
        self.assertEqual(list(response.keys())[0], 'warnings')
        self.assertEqual(response['warnings']['wbgetentities']['*'],
                         'Unrecognized value for parameter "languages": non_existent.')

    @ignore_resource_warnings
    def test_request_with_existent_params_should_return_response(self):
        params = {
            "action": "wbgetentities",
            "ids": "Q66",
            "languages": "en",
            "format": "json"
        }

        under_test = ApiRequestManager()
        response = under_test.get_response(params)
        self.assertEqual(list(response.keys())[0], 'entities')
        self.assertEqual(response['success'], 1)
