from unittest import TestCase, mock

from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
    extract_gbfs_datasets_infos_from_database,
    extract_previous_md5_hashes,
    extract_source_infos,
)
from utilities.constants import (
    STAGING_API_URL,
    STAGING_SPARQL_URL,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    VALUE,
    LABELS,
    ENGLISH,
)


class TestExtractDatabaseMd5(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.wbi_core.ItemEngine")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_dataset_version_codes"
    )
    def test_extract_database_md5_with_existing_entity_codes_should_return_md5_dict(
        self, mock_versions_extractor, mock_item_engine
    ):
        mock_versions_extractor.return_value = {"Q81"}

        test_entity = ["Q80"]
        test_md5 = {"md5_hash"}

        mock_item_engine.return_value.get_json_representation.return_value = {
            CLAIMS: {"P61": [{MAINSNAK: {DATAVALUE: {VALUE: "md5_hash"}}}]}
        }

        under_test = extract_previous_md5_hashes(test_entity)
        self.assertEqual(under_test, test_md5)

    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_dataset_version_codes"
    )
    def test_extract_database_md5_with_non_existing_entity_should_return_empty_md5_dict(
        self, mock_versions_extractor
    ):
        test_entity = ["mock"]
        test_md5 = set()

        mock_versions_extractor.return_value = set()

        under_test = extract_previous_md5_hashes(test_entity)
        self.assertEqual(under_test, test_md5)


class TestExtractInfosTest(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.wbi_core.ItemEngine")
    def test_extract_source_infos_with_default_parameters_should_return_dataset_infos(
        self, mock_item_engine
    ):
        mock_item_engine.return_value.get_json_representation.return_value = {
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
            },
            LABELS: {ENGLISH: {VALUE: "test_name"}},
        }

        (
            under_test_url,
            under_test_name,
        ) = extract_source_infos("Q82")
        self.assertEqual(
            under_test_url, "http://www.stl.laval.qc.ca/opendata/GTF_STL.zip"
        )
        self.assertEqual(under_test_name, "test_name")


class TestExtractDatasetsInfosFromDatabase(TestCase):
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_source_entity_codes"
    )
    @mock.patch("usecase.extract_datasets_infos_from_database.extract_source_infos")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_previous_md5_hashes"
    )
    def test_extract_gtfs_with_valid_parameters_should_return_dataset_infos(
        self,
        mock_md5_extractor,
        mock_source_infos_extractor,
        mock_entity_codes_extractor,
    ):
        mock_entity_codes_extractor.return_value = ["Q80"]
        mock_source_infos_extractor.return_value = "test_url", "test_name"
        mock_md5_extractor.return_value = {"test_md5_hash"}

        under_test = extract_gtfs_datasets_infos_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.url, "test_url")
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(under_test_dataset_info.previous_md5_hashes, {"test_md5_hash"})

    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_source_entity_codes"
    )
    @mock.patch("usecase.extract_datasets_infos_from_database.extract_source_infos")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_previous_md5_hashes"
    )
    def test_extract_gbfs_with_valid_parameters_should_return_dataset_infos(
        self,
        mock_md5_extractor,
        mock_source_infos_extractor,
        mock_entity_codes_extractor,
    ):
        mock_entity_codes_extractor.return_value = ["Q80"]
        mock_source_infos_extractor.return_value = "test_url", "test_name"
        mock_md5_extractor.return_value = {"test_md5_hash"}

        under_test = extract_gbfs_datasets_infos_from_database(
            STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.url, "test_url")
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(under_test_dataset_info.previous_md5_hashes, {"test_md5_hash"})
