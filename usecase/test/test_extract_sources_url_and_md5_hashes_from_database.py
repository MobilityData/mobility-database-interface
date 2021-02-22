from unittest import TestCase, mock
from unittest.mock import Mock

from usecase.extract_sources_url_and_md5_hashes_from_database import (
    extract_gtfs_sources_url_and_md5_hashes_from_database,
    extract_gbfs_sources_url_and_md5_hashes_from_database,
    extract_md5_hashes,
    extract_source_url,
)
from utilities.constants import (
    STAGING_API_URL,
    STAGING_SPARQL_URL,
    ENTITIES,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    VALUE,
    RESULTS,
    BINDINGS,
)


class TestExtractDatabaseMd5(TestCase):
    @mock.patch(
        "usecase.extract_sources_url_and_md5_hashes_from_database.sparql_request"
    )
    @mock.patch("usecase.extract_sources_url_and_md5_hashes_from_database.requests.get")
    def test_extract_database_md5_with_existing_entity_codes_should_return_md5_dict(
        self, mock_api_request, mock_sparkl_request
    ):
        test_entity = ["Q80"]
        test_md5 = {"md5_hash"}

        mock_sparkl_request.return_value = {
            "results": {
                "bindings": [
                    {
                        "a": {
                            "value": "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"
                        }
                    },
                    {
                        "a": {
                            "value": "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"
                        }
                    },
                ]
            }
        }

        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.return_value = {
            ENTITIES: {
                "Q81": {CLAIMS: {"P61": [{MAINSNAK: {DATAVALUE: {VALUE: "md5_hash"}}}]}}
            }
        }
        mock_api_request.return_value.raise_for_status.return_value = None

        under_test = extract_md5_hashes(
            STAGING_API_URL, STAGING_SPARQL_URL, test_entity
        )
        self.assertEqual(under_test, test_md5)

    @mock.patch(
        "usecase.extract_sources_url_and_md5_hashes_from_database.sparql_request"
    )
    @mock.patch("usecase.extract_sources_url_and_md5_hashes_from_database.requests.get")
    def test_extract_database_md5_with_non_existing_entity_should_return_empty_md5_dict(
        self, mock_api_request, mock_sparql_request
    ):
        test_entity = ["mock"]
        test_md5 = set()

        mock_sparql_request.return_value = {RESULTS: {BINDINGS: []}}
        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.return_value = {
            ENTITIES: {
                "Q81": {CLAIMS: {"P61": [{MAINSNAK: {DATAVALUE: {VALUE: "md5_hash"}}}]}}
            }
        }
        mock_api_request.return_value.raise_for_status.return_value = None

        under_test = extract_md5_hashes(
            STAGING_API_URL, STAGING_SPARQL_URL, test_entity
        )
        self.assertEqual(under_test, test_md5)


class TestExtractSourcesUrlTest(TestCase):
    @mock.patch("usecase.extract_sources_url_and_md5_hashes_from_database.requests.get")
    def test_extract_sources_url_with_default_parameters_should_return_urls_dictionary(
        self,
        mock_api_request,
    ):
        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.return_value = {
            ENTITIES: {
                "Q82": {
                    CLAIMS: {
                        "P55": [
                            {
                                MAINSNAK: {
                                    DATAVALUE: {
                                        VALUE: "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
        mock_api_request.return_value.raise_for_status.return_value = None

        under_test = extract_source_url(STAGING_API_URL, "Q82")
        self.assertEqual(under_test, "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip")


class TestExtractSourcesUrlAndMd5HashesFromDatabase(TestCase):
    @mock.patch(
        "usecase.extract_sources_url_and_md5_hashes_from_database.sparql_request"
    )
    @mock.patch("usecase.extract_sources_url_and_md5_hashes_from_database.requests.get")
    def test_extract_gtfs_with_valid_parameters_should_return_urls_and_md5_hashes(
        self, mock_api_request, mock_sparql_request
    ):
        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.side_effect = [
            {
                "entities": {
                    "Q82": {
                        "claims": {
                            "P55": [
                                {
                                    "mainsnak": {
                                        "datavalue": {
                                            "value": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            {
                "entities": {
                    "Q81": {
                        "claims": {
                            "P61": [
                                {"mainsnak": {"datavalue": {"value": "test_md5_hash"}}}
                            ]
                        }
                    }
                }
            },
        ]

        mock_sparql_request.side_effect = [
            {
                "results": {
                    "bindings": [
                        {
                            "a": {
                                "value": "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"
                            }
                        }
                    ]
                }
            },
            {
                "results": {
                    "bindings": [
                        {
                            "a": {
                                "value": "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"
                            }
                        },
                        {
                            "a": {
                                "value": "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"
                            }
                        },
                    ]
                }
            },
        ]

        (
            under_test_urls,
            under_test_md5,
        ) = extract_gtfs_sources_url_and_md5_hashes_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(
            {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}, under_test_urls
        )
        self.assertEqual(under_test_md5, {"Q82": {"test_md5_hash"}})

    @mock.patch(
        "usecase.extract_sources_url_and_md5_hashes_from_database.sparql_request"
    )
    @mock.patch("usecase.extract_sources_url_and_md5_hashes_from_database.requests.get")
    def test_extract_gbfs_with_valid_parameters_should_return_urls_and_md5_hashes(
        self, mock_api_request, mock_sparql_request
    ):
        mock_api_request.return_value.json.side_effect = [
            {
                "entities": {
                    "Q82": {
                        "claims": {
                            "P55": [
                                {
                                    "mainsnak": {
                                        "datavalue": {
                                            "value": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            {
                "entities": {
                    "Q82": {
                        "claims": {
                            "P61": [
                                {"mainsnak": {"datavalue": {"value": "test_md5_hash"}}}
                            ]
                        }
                    }
                }
            },
        ]

        mock_sparql_request.return_value = {
            "results": {
                "bindings": [
                    {
                        "a": {
                            "value": "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"
                        }
                    }
                ]
            }
        }

        (
            under_test_urls,
            under_test_md5,
        ) = extract_gbfs_sources_url_and_md5_hashes_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(
            under_test_urls, {"Q82": "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"}
        )
        self.assertEqual(under_test_md5, {"Q82": {"test_md5_hash"}})
