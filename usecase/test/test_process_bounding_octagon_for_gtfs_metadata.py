import pandas as pd
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_octagon_for_gtfs_metadata,
    STOP_LAT,
    STOP_LON,
)
from utilities.geographical_utils import LAT, LON


class TestProcessBoundingOctagonForGtfsMetadata(TestCase):
    def test_process_bounding_octagon_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_bounding_octagon_for_gtfs_metadata, None)

    def test_process_bounding_octagon_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError,
            process_bounding_octagon_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    def test_process_bounding_octagon_execution_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_bounding_octagon_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.bounding_octagon,
            {},
        )

    def test_process_bounding_octagon_execution_missing_fields(self):
        mock_stops = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_bounding_octagon_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.bounding_octagon,
            {},
        )

    def test_process_bounding_octagon_execution(self):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_bounding_octagon_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(
            mock_metadata.bounding_octagon,
            {
                "1": {LAT: -1, LON: 3},
                "2": {LAT: -3, LON: 1},
                "3": {LAT: -3, LON: -1},
                "4": {LAT: -1, LON: -3},
                "5": {LAT: 1, LON: -3},
                "6": {LAT: 3, LON: -1},
                "7": {LAT: 3, LON: 1},
                "8": {LAT: 1, LON: 3},
            },
        )
