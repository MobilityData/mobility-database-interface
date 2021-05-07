from unittest import TestCase, mock
from unittest.mock import MagicMock

from representation.gtfs_representation import GtfsRepresentation
from representation.gtfs_metadata import GtfsMetadata
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_dataset_entity_for_gtfs_metadata,
)


class TestCreateDatasetEntity(TestCase):
    def test_create_dataset_entity_with_invalid_gtfs_representation(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str

        self.assertRaises(
            TypeError, create_dataset_entity_for_gtfs_metadata, mock_gtfs_representation
        )

    @mock.patch("usecase.create_dataset_entity_for_gtfs_metadata.wbi_login")
    @mock.patch("usecase.create_dataset_entity_for_gtfs_metadata.os.environ")
    @mock.patch("usecase.create_dataset_entity_for_gtfs_metadata.wbi_core")
    def test_create_dataset_entity_with_valid_parameter(
        self, mock_wbi_core, mock_env, mock_wbi_login
    ):
        mock_wbi_core.ItemEngine.return_value.write.return_value = (
            "test_dataset_version_code"
        )

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_metadata = MagicMock()
        mock_gtfs_metadata.__class__ = GtfsMetadata
        type(mock_gtfs_representation).metadata = mock_gtfs_metadata

        under_test = create_dataset_entity_for_gtfs_metadata(
            mock_gtfs_representation, "http://staging.mobilitydatabase.org/w/api.php"
        )
        self.assertEqual(under_test, mock_gtfs_representation)
        self.assertEqual(
            under_test.metadata.dataset_version_entity_code, "test_dataset_version_code"
        )
