import pandas as pd
from unittest import TestCase, mock
from unittest.mock import PropertyMock, MagicMock
from gtfs_kit.feed import Feed
from utilities.geographical_utils import *


class GeographicalUtilsTest(TestCase):

    def test_get_latitude_as_string_with_latitude_float_should_return_latitude_as_string(self):
        mock_latitude = MagicMock()
        mock_latitude.__class__ = float
        mock_latitude.__float__.return_value = 44.508888

        under_test = get_latitude_as_string(float(mock_latitude))
        self.assertEqual(under_test, '44°30\'31.997"N')

    def test_get_longitude_as_string_with_longitude_float_should_return_longitude_as_string(self):
        mock_longitude = MagicMock()
        mock_longitude.__class__ = float
        mock_longitude.__float__.return_value = -74.561668

        under_test = get_longitude_as_string(float(mock_longitude))
        self.assertEqual(under_test, '74°33\'42.005"W')

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_geographical_coordinates_with_dataset_with_stops_should_return_coordinates_as_string(self,
                                                                                                      mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2, under_test_3, under_test_4 = get_geographical_coordinates_as_string(mock_dataset)
        self.assertEqual(under_test_1, '45°30\'31.997"N')
        self.assertEqual(under_test_2, '44°30\'31.997"N')
        self.assertEqual(under_test_3, '73°33\'42.005"W')
        self.assertEqual(under_test_4, '74°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)
