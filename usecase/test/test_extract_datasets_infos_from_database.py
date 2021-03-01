from unittest import TestCase, mock
from unittest.mock import Mock

from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
    extract_gbfs_datasets_infos_from_database,
    extract_previous_md5_hashes,
    extract_source_infos,
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
    LABELS,
    ENGLISH,
    ID,
)


class TestExtractDatabaseMd5(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.sparql_request")
    @mock.patch("usecase.extract_datasets_infos_from_database.requests.get")
    def test_extract_database_md5_with_existing_entity_codes_should_return_md5_dict(
        self, mock_api_request, mock_sparql_request
    ):
        test_entity = ["Q80"]
        test_md5 = {"md5_hash"}

        mock_sparql_request.return_value = {
            RESULTS: {
                BINDINGS: [
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"
                        }
                    },
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"
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

        under_test = extract_previous_md5_hashes(
            STAGING_API_URL, STAGING_SPARQL_URL, test_entity
        )
        self.assertEqual(under_test, test_md5)

    @mock.patch("usecase.extract_datasets_infos_from_database.sparql_request")
    @mock.patch("usecase.extract_datasets_infos_from_database.requests.get")
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

        under_test = extract_previous_md5_hashes(
            STAGING_API_URL, STAGING_SPARQL_URL, test_entity
        )
        self.assertEqual(under_test, test_md5)


class TestExtractInfosTest(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.requests.get")
    def test_extract_source_infos_with_default_parameters_should_return_urls_and_names_dictionary(
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
                        ],
                        "P64": [{MAINSNAK: {DATAVALUE: {VALUE: {ID: "test_version"}}}}],
                    },
                    LABELS: {ENGLISH: {VALUE: "test_name"}},
                }
            }
        }
        mock_api_request.return_value.raise_for_status.return_value = None

        (
            under_test_url,
            under_test_name,
            under_test_previous_versions,
        ) = extract_source_infos(STAGING_API_URL, "Q82")
        self.assertEqual(
            under_test_url, "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"
        )
        self.assertEqual(under_test_name, "test_name")
        self.assertEqual(under_test_previous_versions, {"test_version"})


class TestExtractDatasetsInfosFromDatabase(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.sparql_request")
    @mock.patch("usecase.extract_datasets_infos_from_database.requests.get")
    def test_extract_gtfs_with_valid_parameters_should_return_dataset_infos(
        self, mock_api_request, mock_sparql_request
    ):
        mock_api_request.return_value = Mock()
        mock_api_request.return_value.json.side_effect = [
            {
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
                            ],
                            "P64": [
                                {MAINSNAK: {DATAVALUE: {VALUE: {ID: "test_version"}}}}
                            ],
                        },
                        LABELS: {ENGLISH: {VALUE: "test_name"}},
                    }
                }
            },
            {
                ENTITIES: {
                    "Q81": {
                        CLAIMS: {
                            "P61": [{MAINSNAK: {DATAVALUE: {VALUE: "test_md5_hash"}}}]
                        }
                    }
                }
            },
        ]

        mock_sparql_request.side_effect = [
            {
                RESULTS: {
                    BINDINGS: [
                        {
                            "a": {
                                VALUE: "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"
                            }
                        }
                    ]
                }
            },
            {
                RESULTS: {
                    BINDINGS: [
                        {
                            "a": {
                                VALUE: "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"
                            }
                        },
                        {
                            "a": {
                                VALUE: "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"
                            }
                        },
                    ]
                }
            },
        ]

        under_test = extract_gtfs_datasets_infos_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(
            under_test_dataset_info.url,
            "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip",
        )
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(under_test_dataset_info.previous_md5_hashes, {"test_md5_hash"})
        self.assertEqual(under_test_dataset_info.previous_versions, {"test_version"})

    @mock.patch("usecase.extract_datasets_infos_from_database.sparql_request")
    @mock.patch("usecase.extract_datasets_infos_from_database.requests.get")
    def test_extract_gbfs_with_valid_parameters_should_return_dataset_infos(
        self, mock_api_request, mock_sparql_request
    ):
        mock_api_request.return_value.json.side_effect = [
            {
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
                            ],
                            "P64": [
                                {MAINSNAK: {DATAVALUE: {VALUE: {ID: "test_version"}}}}
                            ],
                        },
                        LABELS: {ENGLISH: {VALUE: "test_name"}},
                    }
                }
            },
            {
                ENTITIES: {
                    "Q82": {
                        CLAIMS: {
                            "P61": [{MAINSNAK: {DATAVALUE: {VALUE: "test_md5_hash"}}}]
                        }
                    }
                }
            },
        ]

        mock_sparql_request.return_value = {
            RESULTS: {
                BINDINGS: [
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"
                        }
                    }
                ]
            }
        }

        under_test = extract_gtfs_datasets_infos_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(
            under_test_dataset_info.url,
            "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip",
        )
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(under_test_dataset_info.previous_md5_hashes, {"test_md5_hash"})
        self.assertEqual(under_test_dataset_info.previous_versions, {"test_version"})
