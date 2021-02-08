from unittest import TestCase, mock
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from usecase.extract_sources_url_and_md5_hashes_from_database import ExtractSourcesUrl


class ExtractSourcesUrlTest(TestCase):

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_none_api_request_manager_should_raise_exception(self,
                                                                                      mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError, ExtractSourcesUrl, None, mock_sparql_request_manager)

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_invalid_api_request_manager_should_raise_exception(self,
                                                                                         mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError, ExtractSourcesUrl, mock_sparql_request_manager, mock_sparql_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_sources_url_with_none_sparql_request_manager_should_raise_exception(self,
                                                                                         mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError, ExtractSourcesUrl, mock_api_request_manager, None)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_sources_url_with_invalid_sparql_request_manager_should_raise_exception(self,
                                                                                            mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError, ExtractSourcesUrl, mock_api_request_manager, mock_api_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_valid_request_managers_should_not_raise_exception(self,
                                                                                        mock_api_request_manager,
                                                                                        mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager)
        self.assertIsInstance(under_test, ExtractSourcesUrl)
        mock_api_request_manager.assert_not_called()
        mock_sparql_request_manager.assert_not_called()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_default_parameters_should_return_urls_dictionary(self,
                                                                                       mock_api_request_manager,
                                                                                       mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = \
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = \
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}

        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager)
        self.assertEqual(under_test.execute(), {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.execute_get.assert_called_once()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_GTFS_dataset_type_should_return_urls_dictionary(self,
                                                                                      mock_api_request_manager,
                                                                                      mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = \
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = \
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}

        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager, dataset_type="GTFS")
        self.assertEqual(under_test.execute(), {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.execute_get.assert_called_once()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_GBFS_dataset_type_should_return_urls_dictionary(self,
                                                                                      mock_api_request_manager,
                                                                                      mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = \
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = \
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}

        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager, dataset_type="GBFS")
        self.assertEqual(under_test.execute(), {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.execute_get.assert_called_once()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_non_existing_specific_dataset_should_return_no_url(self,
                                                                                         mock_api_request_manager,
                                                                                         mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = {'error': {'code': 'no-such-entity'}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager, specific_download=True,
                                       specific_entity_code="Q86")
        self.assertEqual(under_test.execute(), {})
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.assert_not_called()

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_sources_url_with_existing_specific_dataset_should_return_url(self,
                                                                                  mock_api_request_manager,
                                                                                  mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.return_value = \
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        under_test = ExtractSourcesUrl(mock_api_request_manager, mock_sparql_request_manager, specific_download=True,
                                       specific_entity_code="Q82")
        self.assertEqual(under_test.execute(), {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        mock_api_request_manager.execute_get.assert_called_once()
        mock_sparql_request_manager.assert_not_called()
