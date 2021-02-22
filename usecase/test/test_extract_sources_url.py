# from unittest import TestCase, mock
# from unittest.mock import Mock
#
# from usecase.extract_sources_url import extract_source_url
# from utilities.constants import STAGING_API_URL, STAGING_SPARQL_URL
#
#
# class TestExtractSourcesUrlTest(TestCase):
#     @mock.patch('usecase.extract_sources_url.sparql_request')
#     @mock.patch('usecase.extract_sources_url.requests.get')
#     def test_extract_sources_url_with_default_parameters_should_return_urls_dictionary(self,
#                                                                                        mock_api_request,
#                                                                                        mock_sparql_request):
#         mock_api_request.return_value = Mock()
#         mock_api_request.return_value.json.return_value = {
#         "entities": {
#             "Q82": {"claims": {
#                 "P55": [
#                     {"mainsnak": {
#                         "datavalue": {"value": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}
#                     }}
#                 ]
#             }}
#         }
#     }
#         mock_api_request.return_value.raise_for_status.return_value = None
#
#         mock_sparql_request.return_value = {"results": {"bindings": [{"a": {"value":
#              "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}
#         under_test = extract_source_url(STAGING_API_URL,STAGING_SPARQL_URL)
#         self.assertEqual(under_test, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
#
#     @mock.patch('usecase.extract_sources_url.sparql_request')
#     @mock.patch('usecase.extract_sources_url.requests.get')
#     def test_extract_sources_url_with_GTFS_dataset_type_should_return_urls_dictionary(self,
#                                                                                       mock_api_request,
#                                                                                       mock_sparql_request):
#         mock_api_request.return_value = Mock()
#         mock_api_request.return_value.json.return_value = {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
#              "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}
#         mock_api_request.return_value.raise_for_status.return_value = None
#
#
#         mock_sparql_request.return_value =  {"results": {"bindings": [{"a": {"value":
#              "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}
#
#         under_test = extract_source_url(STAGING_API_URL,STAGING_SPARQL_URL, dataset_type="GTFS")
#         self.assertEqual(under_test, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
#
#     @mock.patch('usecase.extract_sources_url.sparql_request')
#     @mock.patch('usecase.extract_sources_url.requests.get')
#     def test_extract_sources_url_with_GBFS_dataset_type_should_return_urls_dictionary(self,
#                                                                                       mock_api_request,
#                                                                                       mock_sparql_request):
#         mock_api_request.return_value = Mock()
#         mock_api_request.return_value.json.return_value = {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
#              "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}
#         mock_api_request.return_value.raise_for_status.return_value = None
#
#         mock_sparql_request.return_value = {"results": {"bindings": [{"a": {"value":
#              "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}
#
#
#         under_test = extract_source_url(STAGING_API_URL,STAGING_SPARQL_URL, dataset_type="GBFS")
#         self.assertEqual(under_test, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
#
#     @mock.patch('usecase.extract_sources_url.sparql_request')
#     @mock.patch('usecase.extract_sources_url.requests.get')
#     def test_extract_sources_url_with_non_existing_specific_dataset_should_return_no_url(self,
#                                                                                          mock_api_request,
#                                                                                          mock_sparql_request):
#         mock_api_request.return_value = Mock()
#         mock_api_request.return_value.json.return_value = {'error': {'code': 'no-such-entity'}}
#         mock_api_request.return_value.raise_for_status.return_value = None
#
#         mock_sparql_request.return_value = {"results": {"bindings": [{"a": {"value":
#                                                                                 "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"}}]}}
#
#         under_test = extract_source_url(STAGING_API_URL,STAGING_SPARQL_URL, specific_download=True,
#                                        specific_entity_code="Q86")
#         self.assertEqual(under_test, {})
#
#     @mock.patch('usecase.extract_sources_url.sparql_request')
#     @mock.patch('usecase.extract_sources_url.requests.get')
#     def test_extract_sources_url_with_existing_specific_dataset_should_return_url(self,
#                                                                                   mock_api_request,
#                                                                                   mock_sparql_request):
#         mock_api_request.return_value = Mock()
#         mock_api_request.return_value.json.return_value = {"entities": {"Q82": {"claims": {"P55": [{"mainsnak": {"datavalue": {"value":
#              "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}}}]}}}}
#         mock_api_request.return_value.raise_for_status.return_value = None
#
#
#         under_test = extract_source_url(STAGING_API_URL,STAGING_SPARQL_URL, specific_download=True,
#                                        specific_entity_code="Q82")
#         self.assertEqual(under_test, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"})
