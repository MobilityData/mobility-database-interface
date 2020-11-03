from unittest import TestCase, mock
from unittest.mock import MagicMock
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from usecase.extract_database_md5 import ExtractDatabaseMd5


class ExtractDatabaseMd5Test(TestCase):

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_none_api_request_manager_should_raise_exception(self,
                                                                                       mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        self.assertRaises(TypeError, ExtractDatabaseMd5, None, mock_sparql_request_manager, mock_entity_codes)

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_invalid_api_request_manager_should_raise_exception(self,
                                                                                          mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        self.assertRaises(TypeError, ExtractDatabaseMd5, mock_sparql_request_manager,
                          mock_sparql_request_manager, mock_entity_codes)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_database_md5_with_none_sparql_request_manager_should_raise_exception(self,
                                                                                         mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        self.assertRaises(TypeError, ExtractDatabaseMd5, mock_api_request_manager, None, mock_entity_codes)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_database_md5_with_invalid_sparql_request_manager_should_raise_exception(self,
                                                                                            mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        self.assertRaises(TypeError, ExtractDatabaseMd5, mock_api_request_manager,
                          mock_api_request_manager, mock_entity_codes)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_none_entity_codes_should_raise_exception(self, mock_api_request_manager,
                                                                                mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError, ExtractDatabaseMd5, mock_api_request_manager, mock_sparql_request_manager, None)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_invalid_entity_codes_should_raise_exception(self, mock_api_request_manager,
                                                                                   mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError, ExtractDatabaseMd5, mock_api_request_manager, mock_sparql_request_manager,
                          mock_sparql_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_valid_parameters_should_not_raise_exception(self, mock_api_request_manager,
                                                                                   mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list

        under_test = ExtractDatabaseMd5(mock_api_request_manager, mock_sparql_request_manager, mock_entity_codes)
        self.assertIsInstance(under_test, ExtractDatabaseMd5)
        mock_api_request_manager.assert_not_called()
        mock_sparql_request_manager.assert_not_called()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_empty_entity_codes_should_return_empty_md5_dict(self, mock_api_request_manager,
                                                                                       mock_sparql_request_manager):
        test_entities = []
        test_md5 = {}

        mock_api_request_manager.__class__ = ApiRequestManager
        mock_sparql_request_manager.__class__ = SparqlRequestManager

        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        mock_entity_codes.__iter__.side_effect = test_entities.__iter__

        under_test = ExtractDatabaseMd5(mock_api_request_manager, mock_sparql_request_manager, mock_entity_codes)
        self.assertEqual(under_test.execute(), test_md5)
        mock_api_request_manager.assert_not_called()
        mock_sparql_request_manager.asser_not_called()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_existing_entity_codes_should_return_md5_dict(self, mock_api_request_manager,
                                                                                    mock_sparql_request_manager):
        test_entities = ['Q81']
        test_md5 = {"Q81": {"md5_hash"}}

        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = \
            {"entities": {"Q81": {"claims": {"P61": [{"mainsnak": {"datavalue": {"value": "md5_hash"}}}]}}}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = \
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"}}]}}

        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        mock_entity_codes.__iter__.side_effect = test_entities.__iter__

        under_test = ExtractDatabaseMd5(mock_api_request_manager, mock_sparql_request_manager, mock_entity_codes)
        self.assertEqual(under_test.execute(), test_md5)
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.execute_get.assert_called_once()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_database_md5_with_non_existing_entity_should_return_empty_md5_dict(self, mock_api_request_manager,
                                                                                        mock_sparql_request_manager):
        test_entities = ['mock']
        test_md5 = {}

        mock_api_request_manager.__class__ = ApiRequestManager

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = {'results': {'bindings': []}}

        mock_entity_codes = MagicMock()
        mock_entity_codes.__class__ = list
        mock_entity_codes.__iter__.side_effect = test_entities.__iter__

        under_test = ExtractDatabaseMd5(mock_api_request_manager, mock_sparql_request_manager, mock_entity_codes)
        self.assertEqual(under_test.execute(), test_md5)
        mock_api_request_manager.asser_not_called()
        mock_sparql_request_manager.execute_get.assert_called_once()

