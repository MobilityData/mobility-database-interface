from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock

from usecase.extract_database_md5 import extract_database_md5
from utilities.constants import STAGING_API_URL, STAGING_SPARQL_URL


class TestExtractDatabaseMd5(TestCase):
    def test_extract_database_md5_empty_dict(self):
        under_test = extract_database_md5(STAGING_API_URL, STAGING_SPARQL_URL, [])
        self.assertEqual(under_test, {})

    @mock.patch('usecase.extract_database_md5.sparql_request')
    @mock.patch('usecase.extract_database_md5.requests.get')
    def test_extract_database_md5_with_existing_entity_codes_should_return_md5_dict(self,mock_api_request, mock_sparkl_request):
        test_entities = ['Q80']
        test_md5 = {"Q80": {"md5_hash"}}

        mock_sparkl_request.return_value = {
            "results": {"bindings": [
                {"a": {"value": "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"}},
                {"a": {"value": "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"}}
            ]}
        }

        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.return_value = {
            "entities": {"Q81": {"claims": {
                "P61": [
                    {"mainsnak": {"datavalue": {"value": "md5_hash"}}}
                ]
            }}}
        }
        mock_api_request.return_value.raise_for_status.return_value = None


        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        mock_entity_codes.__iter__.side_effect = test_entities.__iter__

        under_test = extract_database_md5(STAGING_API_URL, STAGING_SPARQL_URL, mock_entity_codes)
        self.assertEqual(under_test, test_md5)

    @mock.patch('usecase.extract_database_md5.sparql_request')
    @mock.patch('usecase.extract_database_md5.requests.get')
    def test_extract_database_md5_with_non_existing_entity_should_return_empty_md5_dict(self, mock_api_request,
                                                                                        mock_sparql_request):
        test_entities = ['mock']
        test_md5 = {}

        mock_sparql_request.return_value = {'results': {'bindings': []}}
        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.return_value = {
            "entities": {"Q81": {"claims": {
                "P61": [
                    {"mainsnak": {"datavalue": {"value": "md5_hash"}}}
                ]
            }}}
        }
        mock_api_request.return_value.raise_for_status.return_value = None

        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        mock_entity_codes.__iter__.side_effect = test_entities.__iter__

        under_test = extract_database_md5(STAGING_API_URL,STAGING_SPARQL_URL,mock_entity_codes)
        self.assertEqual(under_test, test_md5)

