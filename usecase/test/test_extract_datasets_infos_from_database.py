from unittest import TestCase, mock

from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
    extract_gbfs_datasets_infos_from_database,
    extract_previous_sha1_hashes,
    extract_source_infos,
)
from utilities.constants import (
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    VALUE,
    LABELS,
    ENGLISH,
    STABLE_URL_PROP,
    SHA1_HASH_PROP,
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
)


class TestExtractDatabaseSha1(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.os.environ")
    @mock.patch("usecase.extract_datasets_infos_from_database.wbi_core.ItemEngine")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_dataset_version_codes"
    )
    def test_extract_database_sha1_with_existing_entity_codes_should_return_sha1_dict(
        self, mock_versions_extractor, mock_item_engine, mock_env
    ):
        test_env = {
            SHA1_HASH_PROP: "test_sha1_prop",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__
        mock_versions_extractor.return_value = {"Q81"}

        test_entity = ["Q80"]
        test_sha1 = {"sha1_hash"}

        mock_item_engine.return_value.get_json_representation.return_value = {
            CLAIMS: {"test_sha1_prop": [{MAINSNAK: {DATAVALUE: {VALUE: "sha1_hash"}}}]}
        }

        under_test = extract_previous_sha1_hashes(test_entity)
        self.assertEqual(under_test, test_sha1)

    @mock.patch("usecase.extract_datasets_infos_from_database.os.environ")
    @mock.patch("usecase.extract_datasets_infos_from_database.wbi_core.ItemEngine")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_dataset_version_codes"
    )
    def test_extract_database_sha1_with_None_sha1(
        self, mock_versions_extractor, mock_item_engine, mock_env
    ):
        test_env = {
            SHA1_HASH_PROP: "test_sha1_prop",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__
        mock_versions_extractor.return_value = {"Q81"}

        test_entity = ["Q80"]

        mock_item_engine.return_value.get_json_representation.return_value = {
            CLAIMS: {"test_sha1_prop": [{MAINSNAK: {DATAVALUE: {VALUE: None}}}]}
        }

        under_test = extract_previous_sha1_hashes(test_entity)
        self.assertEqual(under_test, set())

    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_dataset_version_codes"
    )
    def test_extract_database_sha1_with_non_existing_entity_should_return_empty_sha1_dict(
        self, mock_versions_extractor
    ):
        test_entity = ["mock"]
        test_sha1 = set()

        mock_versions_extractor.return_value = set()

        under_test = extract_previous_sha1_hashes(test_entity)
        self.assertEqual(under_test, test_sha1)


class TestExtractInfosTest(TestCase):
    @mock.patch("usecase.extract_datasets_infos_from_database.os.environ")
    @mock.patch("usecase.extract_datasets_infos_from_database.wbi_core.ItemEngine")
    def test_extract_source_infos_with_default_parameters_should_return_dataset_infos(
        self, mock_item_engine, mock_env
    ):
        test_env = {
            STABLE_URL_PROP: "test_url_prop",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__
        mock_item_engine.return_value.get_json_representation.return_value = {
            CLAIMS: {
                "test_url_prop": [
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
    @mock.patch("usecase.extract_datasets_infos_from_database.os.environ")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_source_entity_codes"
    )
    @mock.patch("usecase.extract_datasets_infos_from_database.extract_source_infos")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_previous_sha1_hashes"
    )
    def test_extract_gtfs_with_valid_parameters_should_return_dataset_infos(
        self,
        mock_sha1_extractor,
        mock_source_infos_extractor,
        mock_entity_codes_extractor,
        mock_env,
    ):
        test_env = {
            GTFS_CATALOG_OF_SOURCES_CODE: "test_gtfs_catalog",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__
        mock_entity_codes_extractor.return_value = ["Q80"]
        mock_source_infos_extractor.return_value = "test_url", "test_name"
        mock_sha1_extractor.return_value = {"test_sha1_hash"}

        under_test = extract_gtfs_datasets_infos_from_database()
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.url, "test_url")
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(
            under_test_dataset_info.previous_sha1_hashes, {"test_sha1_hash"}
        )

    @mock.patch("usecase.extract_datasets_infos_from_database.os.environ")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_source_entity_codes"
    )
    @mock.patch("usecase.extract_datasets_infos_from_database.extract_source_infos")
    @mock.patch(
        "usecase.extract_datasets_infos_from_database.extract_previous_sha1_hashes"
    )
    def test_extract_gbfs_with_valid_parameters_should_return_dataset_infos(
        self,
        mock_sha1_extractor,
        mock_source_infos_extractor,
        mock_entity_codes_extractor,
        mock_env,
    ):
        test_env = {
            GBFS_CATALOG_OF_SOURCES_CODE: "test_gbfs_catalog",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__
        mock_entity_codes_extractor.return_value = ["Q80"]
        mock_source_infos_extractor.return_value = "test_url", "test_name"
        mock_sha1_extractor.return_value = {"test_sha1_hash"}

        under_test = extract_gbfs_datasets_infos_from_database()
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.url, "test_url")
        self.assertEqual(under_test_dataset_info.source_name, "test_name")
        self.assertEqual(
            under_test_dataset_info.previous_sha1_hashes, {"test_sha1_hash"}
        )
