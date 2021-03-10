import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_box_for_gtfs_metadata,
)
from utilities.geographical_utils import LAT, LON


class TestProcessBoundingBoxForGtfsMetadata(TestCase):
    def test_process_bounding_box_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_bounding_box_for_gtfs_metadata, None)

    def test_process_bounding_box_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError, process_bounding_box_for_gtfs_metadata, mock_gtfs_representation
        )

    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
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
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_bounding_box_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)
        self.assertEqual(
            mock_metadata.bounding_box,
            {
                "1": {LAT: 45.508888, LON: -73.561668},
                "2": {LAT: 45.508888, LON: -73.561668},
                "3": {LAT: 45.508888, LON: -73.561668},
                "4": {LAT: 45.508888, LON: -73.561668},
            },
        )
