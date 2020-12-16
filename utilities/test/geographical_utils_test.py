import pandas as pd
from unittest import TestCase, mock
from unittest.mock import PropertyMock
from gtfs_kit.feed import Feed
from utilities.geographical_utils import *


class GeographicalUtilsTest(TestCase):

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_maximum_latitude_as_string_with_dataset_with_stops_should_return_latitude_as_string(self,
                                                                                                     mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test = get_maximum_latitude_as_string(mock_dataset.stops)
        self.assertEqual(under_test, '45°30\'31.997"N')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_minimum_latitude_as_string_with_dataset_with_stops_should_return_latitude_as_string(self,
                                                                                                     mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test = get_minimum_latitude_as_string(mock_dataset.stops)
        self.assertEqual(under_test, '44°30\'31.997"N')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_maximum_longitude_as_string_with_dataset_with_stops_should_return_longitude_as_string(self,
                                                                                                       mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test = get_maximum_longitude_as_string(mock_dataset.stops)
        self.assertEqual(under_test, '73°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_minimum_longitude_as_string_with_dataset_with_stops_should_return_longitude_as_string(self,
                                                                                                       mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test = get_minimum_longitude_as_string(mock_dataset.stops)
        self.assertEqual(under_test, '74°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_geographical_coordinates_with_dataset_with_stops_should_return_coordinates_as_string(self,
                                                                                                      mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2, under_test_3, under_test_4 = get_geographical_coordinates(mock_dataset)
        self.assertEqual(under_test_1, '45°30\'31.997"N')
        self.assertEqual(under_test_2, '44°30\'31.997"N')
        self.assertEqual(under_test_3, '73°33\'42.005"W')
        self.assertEqual(under_test_4, '74°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 4)
