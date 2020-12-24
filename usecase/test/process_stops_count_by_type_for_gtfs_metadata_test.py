import pandas as pd
import numpy as np
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_stops_count_by_type_for_gtfs_metadata import ProcessStopsCountByTypeForGtfsMetadata


class ProcessStopsCountByTypeForGtfsMetadataTest(TestCase):

    def test_process_stops_count_with_none_gtfs_representation_should_raise_exception(self):
        self.assertRaises(TypeError, ProcessStopsCountByTypeForGtfsMetadata, None)

    def test_process_stops_count_with_invalid_gtfs_representation_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(TypeError, ProcessStopsCountByTypeForGtfsMetadata, mock_gtfs_representation)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    def test_process_stops_count_with_valid_gtfs_representation_should_return_instance(self, mock_gtfs_representation):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = ProcessStopsCountByTypeForGtfsMetadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, ProcessStopsCountByTypeForGtfsMetadata)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_process_stops_count_execution_should_set_start_agencies_count_metadata(self, mock_gtfs_representation,
                                                                                     mock_dataset, mock_metadata):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'location_type': [0, 2, 1, 0, 0, 1, 0, 0, np.nan]}))

        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_representation.get_dataset.return_value = mock_dataset

        under_test = ProcessStopsCountByTypeForGtfsMetadata(mock_gtfs_representation).execute()
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_gtfs_representation.get_dataset.assert_called_once()
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 10)
        mock_gtfs_representation.set_metadata_stops_count_by_type.assert_called_with({'stop': 6,
                                                                                      'station': 2,
                                                                                      'entrance': 1})
