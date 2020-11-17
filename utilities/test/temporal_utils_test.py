from datetime import datetime
import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from utilities.temporal_utils import *


class TemporalUtilsTest(TestCase):

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_dataset_with_none_calendars_should_return_empty_dataframe(self, mock_dataset):
        mock_calendar = PropertyMock(return_value=None)
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_date_type = MagicMock()
        mock_date_type.__class__ = str
        mock_date_type.__str__.return_value = 'test_type'

        under_test = get_gtfs_dates_by_type(mock_dataset, str(mock_date_type))
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 1)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)
        mock_date_type.assert_not_called()

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_none_date_type_and_calendar_dates_should_return_empty_dataframe(self,
                                                                                                        mock_dataset):
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
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        under_test = get_gtfs_dates_by_type(mock_dataset, None)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 1)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_invalid_type_and_none_calendar_dates_should_return_empty_frame(self,
                                                                                                       mock_dataset):
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
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_date_type = MagicMock()
        mock_date_type.__class__ = str
        mock_date_type.__str__.return_value = 'invalid_type'

        under_test = get_gtfs_dates_by_type(mock_dataset, str(mock_date_type))
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 1)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_calendar_and_none_calendar_dates_should_return_dataframe(self, mock_dataset):
        mock_calendar = PropertyMock(return_value=pd.DataFrame({'start_date': ['20201010'],
                                                                'monday': [0],
                                                                'tuesday': [0],
                                                                'wednesday': [0],
                                                                'thursday': [0],
                                                                'friday': [0],
                                                                'saturday': [1],
                                                                'sunday': [0],
                                                                'service_id': ['test_service_id']}))
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_date_type = MagicMock()
        mock_date_type.__class__ = str
        mock_date_type.__str__.return_value = 'start_date'

        test_dataframe = pd.DataFrame({'service_id': ['test_service_id'], 'date': ['20201010']})

        under_test = get_gtfs_dates_by_type(mock_dataset, str(mock_date_type))
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertEqual(under_test['service_id'].all(), test_dataframe['service_id'].all())
        self.assertEqual(under_test['date'].all(), test_dataframe['date'].all())
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 2)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_calendar_dates_with_exception_1_should_return_dataframe(self, mock_dataset):
        mock_calendar = PropertyMock(return_value=None)
        mock_calendar_dates = PropertyMock(return_value=pd.DataFrame({'date': ['20201010'],
                                                                      'exception_type': [1],
                                                                      'service_id': ['test_service_id']}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_date_type = MagicMock()
        mock_date_type.__class__ = str
        mock_date_type.__str__.return_value = 'start_date'

        test_dataframe = pd.DataFrame({'service_id': ['test_service_id'], 'date': ['20201010']})

        under_test = get_gtfs_dates_by_type(mock_dataset, str(mock_date_type))
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertEqual(under_test['service_id'].all(), test_dataframe['service_id'].all())
        self.assertEqual(under_test['date'].all(), test_dataframe['date'].all())
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 1)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 2)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_date_by_type_with_calendar_dates_with_exception_2_should_return_empty_dataframe(self,
                                                                                                      mock_dataset):
        mock_calendar = PropertyMock(return_value=pd.DataFrame({'end_date': ['20201010'],
                                                                'monday': [0],
                                                                'tuesday': [0],
                                                                'wednesday': [0],
                                                                'thursday': [0],
                                                                'friday': [0],
                                                                'saturday': [1],
                                                                'sunday': [0],
                                                                'service_id': ['test_service_id']}))
        mock_calendar_dates = PropertyMock(return_value=pd.DataFrame({'date': ['20201010'],
                                                                      'exception_type': [2],
                                                                      'service_id': ['test_service_id']}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_date_type = MagicMock()
        mock_date_type.__class__ = str
        mock_date_type.__str__.return_value = 'end_date'

        under_test = get_gtfs_dates_by_type(mock_dataset, str(mock_date_type))
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 2)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 2)

    def test_get_gtfs_start_dates_from_calendar_with_empty_calendar_should_return_empty_dataframe(self):
        test_calendar = pd.DataFrame({'start_date': [],
                                      'monday': [],
                                      'tuesday': [],
                                      'wednesday': [],
                                      'thursday': [],
                                      'friday': [],
                                      'saturday': [],
                                      'sunday': [],
                                      'service_id': []})
        mock_calendar = MagicMock()
        mock_calendar.__class__ = pd.DataFrame
        mock_calendar.iterrows.return_value = test_calendar.iterrows()

        test_dataframe = pd.DataFrame(columns=['service_id', 'date'])

        under_test = get_gtfs_start_dates_from_calendar(mock_calendar, test_dataframe)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)

    def test_get_gtfs_start_dates_from_calendar_with_filled_calendar_should_return_empty_dataframe(self):
        test_calendar = pd.DataFrame({'start_date': ['20201010'],
                                      'monday': [1],
                                      'tuesday': [1],
                                      'wednesday': [1],
                                      'thursday': [1],
                                      'friday': [1],
                                      'saturday': [1],
                                      'sunday': [1],
                                      'service_id': ['test_service_date']})
        mock_calendar = MagicMock()
        mock_calendar.__class__ = pd.DataFrame
        mock_calendar.iterrows.return_value = test_calendar.iterrows()

        test_dataframe = pd.DataFrame(columns=['service_id', 'date'])

        test_service_ids_list = ['test_service_date', 'test_service_date', 'test_service_date', 'test_service_date',
                                 'test_service_date', 'test_service_date', 'test_service_date']
        test_dates_list = ['20201012', '20201013', '20201014', '20201015', '20201016', '20201010', '20201011']

        under_test = get_gtfs_start_dates_from_calendar(mock_calendar, test_dataframe)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertEqual(under_test['service_id'].count(), 7)
        self.assertEqual(under_test['service_id'].tolist(), test_service_ids_list)
        self.assertEqual(under_test['date'].count(), 7)
        self.assertEqual(under_test['date'].tolist(), test_dates_list)

    def test_get_gtfs_end_dates_from_calendar_with_empty_calendar_should_return_empty_dataframe(self):
        test_calendar = pd.DataFrame({'end_date': [],
                                      'monday': [],
                                      'tuesday': [],
                                      'wednesday': [],
                                      'thursday': [],
                                      'friday': [],
                                      'saturday': [],
                                      'sunday': [],
                                      'service_id': []})
        mock_calendar = MagicMock()
        mock_calendar.__class__ = pd.DataFrame
        mock_calendar.iterrows.return_value = test_calendar.iterrows()

        test_dataframe = pd.DataFrame(columns=['service_id', 'date'])

        under_test = get_gtfs_end_dates_from_calendar(mock_calendar, test_dataframe)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue(under_test.empty)

    def test_get_gtfs_end_dates_from_calendar_with_filled_calendar_should_return_empty_dataframe(self):
        test_calendar = pd.DataFrame({'end_date': ['20201010'],
                                      'monday': [1],
                                      'tuesday': [1],
                                      'wednesday': [1],
                                      'thursday': [1],
                                      'friday': [1],
                                      'saturday': [1],
                                      'sunday': [1],
                                      'service_id': ['test_service_date']})
        mock_calendar = MagicMock()
        mock_calendar.__class__ = pd.DataFrame
        mock_calendar.iterrows.return_value = test_calendar.iterrows()

        test_dataframe = pd.DataFrame(columns=['service_id', 'date'])

        test_service_ids_list = ['test_service_date', 'test_service_date', 'test_service_date', 'test_service_date',
                                 'test_service_date', 'test_service_date', 'test_service_date']
        test_dates_list = ['20201005', '20201006', '20201007', '20201008', '20201009', '20201010', '20201004']

        under_test = get_gtfs_end_dates_from_calendar(mock_calendar, test_dataframe)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertEqual(under_test['service_id'].count(), 7)
        self.assertEqual(under_test['service_id'].tolist(), test_service_ids_list)
        self.assertEqual(under_test['date'].count(), 7)
        self.assertEqual(under_test['date'].tolist(), test_dates_list)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_gtfs_timezone_utc_offset_with_valid_agency_timezone_should_return_timezone_utc_offset(self,
                                                                                                       mock_dataset):
        mock_agency = PropertyMock(return_value=pd.DataFrame({'agency_timezone': ['America/Montreal']}))

        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        test_utc_offset = '-05:00'

        under_test = get_gtfs_timezone_utc_offset(mock_dataset)
        self.assertEqual(under_test, test_utc_offset)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_gtfs_stop_times_for_date_with_valid_parameters_should_return_stop_times_dataframe(self, mock_dataset):
        mock_trips = PropertyMock(return_value=pd.DataFrame({'service_id': ['test_service_id'],
                                                             'trip_id': ['test_trip_id']}))
        mock_stop_times = PropertyMock(return_value=pd.DataFrame({'trip_id': ['test_trip_id'],
                                                                  'departure_time': ['05:00:00']}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).stop_times = mock_stop_times

        test_dataset_dates = pd.DataFrame({'service_id': ['test_service_id', 'test_service_id', 'test_service_id',
                                                          'test_service_id', 'test_service_id', 'test_service_id',
                                                          'test_service_id'],
                                           'date': ['20201005', '20201006', '20201007', '20201008', '20201009',
                                                    '20201010', '20201004']})
        mock_dataset_dates = MagicMock()
        mock_dataset_dates.__class__ = pd.DataFrame
        mock_dataset_dates.__getitem__.side_effect = test_dataset_dates.__getitem__
        mock_dataset_dates.loc.__getitem__.side_effect = test_dataset_dates.loc.__getitem__
        mock_dataset_dates.items.return_value = test_dataset_dates.items()

        mock_date_to_look_up = MagicMock()
        mock_date_to_look_up.__class__ = datetime
        mock_date_to_look_up.strftime.return_value = '20201010'

        test_stop_times_trip_ids = ['test_trip_id']
        test_stop_times_departure_time = ['05:00:00']

        under_test = get_gtfs_stop_times_for_date(mock_dataset, mock_dataset_dates, mock_date_to_look_up)
        self.assertIsInstance(under_test, pd.DataFrame)
        self.assertTrue('trip_id' in under_test.columns)
        self.assertTrue('departure_time' in under_test.columns)
        self.assertEqual(under_test['trip_id'].tolist(), test_stop_times_trip_ids)
        self.assertEqual(under_test['departure_time'].tolist(), test_stop_times_departure_time)













