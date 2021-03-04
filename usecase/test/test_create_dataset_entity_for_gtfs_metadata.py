from unittest import TestCase, mock
from unittest.mock import MagicMock

from representation.gtfs_representation import GtfsRepresentation
from representation.gtfs_metadata import GtfsMetadata
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_dataset_entity_for_gtfs_metadata,
    create_prop_dict,
)
from utilities.constants import STAGING_API_URL


class TestPropertyDictionaryCreationForDatasetEntityCreation(TestCase):
    def test_create_property_dictionary_with_valid_parameters_should_return_data(self):
        test_datatype = "test_datatype"
        test_prop_id = "test_prop_id"
        test_value = "test_value"
        test_rank = "test_rank"
        test_if_exists = "test_if_exists"

        test_prop_dict = {
            "datatype": "test_datatype",
            "prop_id": "test_prop_id",
            "value": "test_value",
            "rank": "test_rank",
            "if_exists": "test_if_exists",
        }

        under_test = create_prop_dict(
            test_datatype, test_prop_id, test_value, test_rank, test_if_exists
        )
        self.assertEqual(under_test, test_prop_dict)


class TestCreateDatasetEntity(TestCase):
    def test_create_dataset_entity_with_invalid_api_url_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation

        test_api_url = "test_api_url"

        self.assertRaises(
            TypeError,
            create_dataset_entity_for_gtfs_metadata,
            mock_gtfs_representation,
            test_api_url,
        )

    def test_create_dataset_entity_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str

        self.assertRaises(
            TypeError,
            create_dataset_entity_for_gtfs_metadata,
            mock_gtfs_representation,
            STAGING_API_URL,
        )

    @mock.patch("usecase.create_dataset_entity_for_gtfs_metadata.import_entity")
    def test_create_dataset_entity_with_valid_parameter_should_post_request_and_return_representation(
        self, mock_importer
    ):
        mock_importer.side_effect = [
            "test_dataset_version_code",
            "test_source_entity_code",
        ]

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_metadata = MagicMock()
        mock_gtfs_metadata.__class__ = GtfsMetadata
        type(mock_gtfs_representation).metadata = mock_gtfs_metadata

        under_test = create_dataset_entity_for_gtfs_metadata(
            mock_gtfs_representation, STAGING_API_URL
        )
        self.assertEqual(under_test, mock_gtfs_representation)
        self.assertEqual(
            under_test.metadata.dataset_version_entity_code, "test_dataset_version_code"
        )
