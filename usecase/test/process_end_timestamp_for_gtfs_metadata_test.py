import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_end_timestamp_for_gtfs_metadata import ProcessEndTimestampForGtfsMetadata


class ProcessEndTimestampForGtfsMetadataTest(TestCase):

    def test_process_end_timestamp_with_none_gtfs_representation_should_raise_exception(self):
        self.assertRaises(TypeError, ProcessEndTimestampForGtfsMetadata, None)

    def test_process_end_timestamp_with_invalid_gtfs_representation_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(TypeError, ProcessEndTimestampForGtfsMetadata, mock_gtfs_representation)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    def test_process_end_timestamp_with_valid_gtfs_representation_should_return_instance(self,
                                                                                           mock_gtfs_representation):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = ProcessEndTimestampForGtfsMetadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, ProcessEndTimestampForGtfsMetadata)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_process_end_timestamp_execution_should_set_start_timestamp_metadata(self, mock_gtfs_representation,
                                                                                 mock_dataset, mock_metadata):
        mock_calendar = PropertyMock(return_value=pd.DataFrame({'end_date': ['20201010'],
                                                                'monday': [0],
                                                                'tuesday': [0],
                                                                'wednesday': [0],
                                                                'thursday': [0],
                                                                'friday': [0],
                                                                'saturday': [1],
                                                                'sunday': [0],
                                                                'service_id': ['test_service_id']}))
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_trips = PropertyMock(return_value=pd.DataFrame({'service_id': ['test_service_id'],
                                                             'trip_id': ['test_trip_id']}))
        mock_stop_times = PropertyMock(return_value=pd.DataFrame({'trip_id': ['test_trip_id'],
                                                                  'departure_time': ['05:00:00']}))
        mock_agency = PropertyMock(return_value=pd.DataFrame({'agency_timezone': ['America/Montreal']}))

        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).agency = mock_agency

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_representation.get_dataset.return_value = mock_dataset

        under_test = ProcessEndTimestampForGtfsMetadata(mock_gtfs_representation).execute()
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_gtfs_representation.get_dataset.assert_called_once()
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 2)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)
        mock_trips.assert_called()
        self.assertEqual(mock_trips.call_count, 2)
        mock_stop_times.assert_called()
        self.assertEqual(mock_stop_times.call_count, 2)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        mock_gtfs_representation.set_metadata_end_timestamp.assert_called_with('2020-10-10T05:00:00-05:00')
