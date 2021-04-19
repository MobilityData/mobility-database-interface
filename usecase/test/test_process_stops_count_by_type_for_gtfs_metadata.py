import pandas as pd
import numpy as np
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_stops_count_by_type_for_gtfs_metadata import (
    process_stops_count_by_type_for_gtfs_metadata,
    LOCATION_TYPE,
)


class TestProcessStopsCountByTypeForGtfsMetadata(TestCase):
    def test_process_stops_count_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(
            TypeError, process_stops_count_by_type_for_gtfs_metadata, None
        )

    def test_process_stops_count_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError,
            process_stops_count_by_type_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    def test_process_stops_count_with_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_stops_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.stops_count_by_type,
            {},
        )

    def test_process_stops_count_with_missing_fields(self):
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

        under_test = process_stops_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.stops_count_by_type,
            {},
        )

    def test_process_stops_count_execution_should_set_start_agencies_count_metadata(
        self,
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame({LOCATION_TYPE: [0, 2, 1, 0, 0, 1, 0, 0, np.nan]})
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

        under_test = process_stops_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(
            mock_metadata.stops_count_by_type, {"stop": 6, "station": 2, "entrance": 1}
        )
