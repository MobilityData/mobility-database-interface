import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_bounding_box_for_gtfs_metadata import (
    ProcessBoundingBoxForGtfsMetadata,
)


class ProcessBoundingBoxForGtfsMetadataTest(TestCase):
    def test_process_bounding_box_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, ProcessBoundingBoxForGtfsMetadata, None)

    def test_process_bounding_box_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError, ProcessBoundingBoxForGtfsMetadata, mock_gtfs_representation
        )

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_process_bounding_box_with_valid_gtfs_representation_should_return_instance(
        self, mock_gtfs_representation
    ):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = ProcessBoundingBoxForGtfsMetadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, ProcessBoundingBoxForGtfsMetadata)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_bounding_box_execution_should_set_bounding_box_metadata(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {"stop_lat": [45.508888], "stop_lon": [-73.561668]}
            )
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_representation.get_dataset.return_value = mock_dataset

        under_test = ProcessBoundingBoxForGtfsMetadata(
            mock_gtfs_representation
        ).execute()
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_gtfs_representation.get_dataset.assert_called_once()
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)
        mock_gtfs_representation.set_metadata_bounding_box.assert_called_with(
            {
                "1": "45°30'31.997\"N, 73°33'42.005\"W",
                "2": "45°30'31.997\"N, 73°33'42.005\"W",
                "3": "45°30'31.997\"N, 73°33'42.005\"W",
                "4": "45°30'31.997\"N, 73°33'42.005\"W",
            }
        )
