from unittest import TestCase, mock
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from usecase.extract_sources_url_and_md5_hashes_from_database import (
    extract_gtfs_sources_url_and_md5_hashes_from_database,
    extract_gbfs_sources_url_and_md5_hashes_from_database,
)


class TestExtractSourcesUrlAndMd5HashesFromDatabase(TestCase):

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gtfs_with_none_api_request_manager_should_raise_exception(self, mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError,
                          extract_gtfs_sources_url_and_md5_hashes_from_database,
                          None,
                          mock_sparql_request_manager)

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gtfs_with_invalid_api_request_manager_should_raise_exception(self, mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError,
                          extract_gtfs_sources_url_and_md5_hashes_from_database,
                          mock_sparql_request_manager,
                          mock_sparql_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_gtfs_with_none_sparql_request_manager_should_raise_exception(self, mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError,
                          extract_gtfs_sources_url_and_md5_hashes_from_database,
                          mock_api_request_manager,
                          None)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_gtfs_with_invalid_sparql_request_manager_should_raise_exception(self, mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError,
                          extract_gtfs_sources_url_and_md5_hashes_from_database,
                          mock_api_request_manager,
                          mock_api_request_manager)


    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gtfs_with_valid_parameters_should_return_urls_and_md5_hashes(self,
                                                                                  mock_api_request_manager,
                                                                                  mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.side_effect = [
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}},
            {"entities": {"Q81": {"claims": {"P61": [{"mainsnak": {"datavalue": {"value":
              "test_md5_hash"}}}]}}}}
        ]

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.side_effect = [
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}},
            {"results": {"bindings": [
                {"a": {"value": "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"}},
                {"a": {"value": "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"}}
            ]}}
        ]

        under_test_urls, under_test_md5 = extract_gtfs_sources_url_and_md5_hashes_from_database(
            mock_api_request_manager,
            mock_sparql_request_manager
        )
        self.assertEqual(under_test_urls, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        self.assertEqual(under_test_md5, {"Q82": {"test_md5_hash"}})
        mock_api_request_manager.execute_get.assert_called()
        self.assertEqual(mock_api_request_manager.execute_get.call_count, 2)
        mock_sparql_request_manager.execute_get.assert_called()
        self.assertEqual(mock_sparql_request_manager.execute_get.call_count, 2)

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gbfs_with_none_api_request_manager_should_raise_exception(self, mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError,
                          extract_gbfs_sources_url_and_md5_hashes_from_database,
                          None,
                          mock_sparql_request_manager)

    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gbfs_with_invalid_api_request_manager_should_raise_exception(self, mock_sparql_request_manager):
        mock_sparql_request_manager.__class__ = SparqlRequestManager
        self.assertRaises(TypeError,
                          extract_gbfs_sources_url_and_md5_hashes_from_database,
                          mock_sparql_request_manager,
                          mock_sparql_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_gbfs_with_none_sparql_request_manager_should_raise_exception(self, mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError,
                          extract_gbfs_sources_url_and_md5_hashes_from_database,
                          mock_api_request_manager,
                          None)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    def test_extract_gbfs_with_invalid_sparql_request_manager_should_raise_exception(self, mock_api_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        self.assertRaises(TypeError,
                          extract_gbfs_sources_url_and_md5_hashes_from_database,
                          mock_api_request_manager,
                          mock_api_request_manager)

    @mock.patch('request_manager.api_request_manager.ApiRequestManager')
    @mock.patch('request_manager.sparql_request_manager.SparqlRequestManager')
    def test_extract_gbfs_with_valid_parameters_should_return_urls_and_md5_hashes(self,
                                                                                  mock_api_request_manager,
                                                                                  mock_sparql_request_manager):
        mock_api_request_manager.__class__ = ApiRequestManager
        mock_api_request_manager.execute_get.side_effect = [
            {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
             "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}},
            {"entities": {"Q82": {"claims": {"P61": [{"mainsnak": {"datavalue": {"value":
             "test_md5_hash"}}}]}}}}
        ]

        mock_sparql_request_manager.__class__ = SparqlRequestManager
        mock_sparql_request_manager.execute_get.return_value = \
            {"results": {"bindings": [{"a": {"value":
             "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}

        under_test_urls, under_test_md5 = extract_gbfs_sources_url_and_md5_hashes_from_database(
            mock_api_request_manager,
            mock_sparql_request_manager
        )
        self.assertEqual(under_test_urls, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
        self.assertEqual(under_test_md5, {"Q82": {"test_md5_hash"}})
        mock_api_request_manager.execute_get.assert_called()
        self.assertEqual(mock_api_request_manager.execute_get.call_count, 2)
        mock_sparql_request_manager.execute_get.assert_called()
        self.assertEqual(mock_sparql_request_manager.execute_get.call_count, 2)
