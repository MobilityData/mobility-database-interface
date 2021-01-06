import pandas as pd
from unittest import TestCase, mock
from unittest.mock import PropertyMock, MagicMock
from gtfs_kit.feed import Feed
from LatLon23 import Latitude, Longitude
from utilities.geographical_utils import *


class GeographicalUtilsTest(TestCase):

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_box_corners_coordinates_as_string_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2, under_test_3, under_test_4 = get_box_corners_coordinates_as_string(mock_dataset)

        self.assertEqual(under_test_1, '44°30\'31.997"N, 73°33\'42.005"W')
        self.assertEqual(under_test_2, '44°30\'31.997"N, 74°33\'42.005"W')
        self.assertEqual(under_test_3, '45°30\'31.997"N, 74°33\'42.005"W')
        self.assertEqual(under_test_4, '45°30\'31.997"N, 73°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_octagon_corners_coordinates_as_string_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [3, -3, 0, 0, 2, -2, 2, -2],
                                                             'stop_lon': [0, 0, 3, -3, 2, 2, -2, -2]}))
        type(mock_dataset).stops = mock_stops

        under_test = get_octagon_corners_coordinates_as_string(mock_dataset)
        under_test_1 = under_test[0]
        under_test_2 = under_test[1]
        under_test_3 = under_test[2]
        under_test_4 = under_test[3]
        under_test_5 = under_test[4]
        under_test_6 = under_test[5]
        under_test_7 = under_test[6]
        under_test_8 = under_test[7]

        self.assertEqual(under_test_1, '1°0\'0.000"S, 3°0\'0.000"E')
        self.assertEqual(under_test_2, '3°0\'0.000"S, 1°0\'0.000"E')
        self.assertEqual(under_test_3, '3°0\'0.000"S, 1°0\'0.000"W')
        self.assertEqual(under_test_4, '1°0\'0.000"S, 3°0\'0.000"W')
        self.assertEqual(under_test_5, '1°0\'0.000"N, 3°0\'0.000"W')
        self.assertEqual(under_test_6, '3°0\'0.000"N, 1°0\'0.000"W')
        self.assertEqual(under_test_7, '3°0\'0.000"N, 1°0\'0.000"E')
        self.assertEqual(under_test_8, '1°0\'0.000"N, 3°0\'0.000"E')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 5)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_geographical_coordinates_as_string_should_return_coordinates_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2, under_test_3, under_test_4 = \
            get_geographical_coordinates_as_string(mock_dataset.stops)

        self.assertEqual(under_test_1, '45°30\'31.997"N')
        self.assertEqual(under_test_2, '44°30\'31.997"N')
        self.assertEqual(under_test_3, '73°33\'42.005"W')
        self.assertEqual(under_test_4, '74°33\'42.005"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_geographical_coordinates_as_float_should_return_coordinates_as_float(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [45.508888, 44.508888],
                                                             'stop_lon': [-73.561668, -74.561668]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2, under_test_3, under_test_4 = \
            get_geographical_coordinates_as_float(mock_dataset.stops)

        self.assertEqual(under_test_1, 45.508888)
        self.assertEqual(under_test_2, 44.508888)
        self.assertEqual(under_test_3, -73.561668)
        self.assertEqual(under_test_4, -74.561668)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    def test_get_latitude_as_string_with_latitude_float_should_return_latitude_as_string(self):
        mock_latitude = MagicMock()
        mock_latitude.__float__.return_value = 44.508888

        under_test = get_latitude_as_string(float(mock_latitude))
        self.assertEqual(under_test, '44°30\'31.997"N')

    def test_get_longitude_as_string_with_longitude_float_should_return_longitude_as_string(self):
        mock_longitude = MagicMock()
        mock_longitude.__float__.return_value = -74.561668

        under_test = get_longitude_as_string(float(mock_longitude))
        self.assertEqual(under_test, '74°33\'42.005"W')

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_upper_right_octagon_corners_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [3, -3, 0, 0, 2, -2, 2, -2],
                                                             'stop_lon': [0, 0, 3, -3, 2, 2, -2, -2]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = get_upper_right_octagon_corners(mock_dataset.stops, 3, 3)

        self.assertEqual(under_test_1, '3°0\'0.000"N, 1°0\'0.000"E')
        self.assertEqual(under_test_2, '1°0\'0.000"N, 3°0\'0.000"E')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_lower_right_octagon_corners_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [3, -3, 0, 0, 2, -2, 2, -2],
                                                             'stop_lon': [0, 0, 3, -3, 2, 2, -2, -2]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = get_lower_right_octagon_corners(mock_dataset.stops, -3, 3)

        self.assertEqual(under_test_1, '3°0\'0.000"S, 1°0\'0.000"E')
        self.assertEqual(under_test_2, '1°0\'0.000"S, 3°0\'0.000"E')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_lower_left_octagon_corners_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [3, -3, 0, 0, 2, -2, 2, -2],
                                                             'stop_lon': [0, 0, 3, -3, 2, 2, -2, -2]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = get_lower_left_octagon_corners(mock_dataset.stops, -3, -3)

        self.assertEqual(under_test_1, '3°0\'0.000"S, 1°0\'0.000"W')
        self.assertEqual(under_test_2, '1°0\'0.000"S, 3°0\'0.000"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_get_upper_left_octagon_corners_should_return_corners_as_string(self, mock_dataset):
        mock_stops = PropertyMock(return_value=pd.DataFrame({'stop_lat': [3, -3, 0, 0, 2, -2, 2, -2],
                                                             'stop_lon': [0, 0, 3, -3, 2, 2, -2, -2]}))
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = get_upper_left_octagon_corners(mock_dataset.stops, 3, -3)

        self.assertEqual(under_test_1, '3°0\'0.000"N, 1°0\'0.000"W')
        self.assertEqual(under_test_2, '1°0\'0.000"N, 3°0\'0.000"W')
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    def test_convert_geographical_coordinates_to_box_corners_should_return_corners_string(self):
        mock_max_lat = MagicMock()
        mock_max_lat.__str__.return_value = '45°30\'31.997"N'

        mock_min_lat = MagicMock()
        mock_min_lat.__str__.return_value = '44°30\'31.997"N'

        mock_max_lon = MagicMock()
        mock_max_lon.__str__.return_value = '73°33\'42.005"W'

        mock_min_lon = MagicMock()
        mock_min_lon.__str__.return_value = '74°33\'42.005"W'

        under_test_1, under_test_2, under_test_3, under_test_4 = \
            convert_geographical_coordinates_to_box_corners_string(str(mock_max_lat), str(mock_min_lat),
                                                                   str(mock_max_lon), str(mock_min_lon))

        self.assertEqual(under_test_1, '44°30\'31.997"N, 73°33\'42.005"W')
        self.assertEqual(under_test_2, '44°30\'31.997"N, 74°33\'42.005"W')
        self.assertEqual(under_test_3, '45°30\'31.997"N, 74°33\'42.005"W')
        self.assertEqual(under_test_4, '45°30\'31.997"N, 73°33\'42.005"W')

    def test_convert_octagon_section_corners_coordinates_to_string_should_return_corners_string(self):
        mock_corner_1_lat = MagicMock()
        mock_corner_1_lat.__float__.return_value = 3.0

        mock_corner_1_lon = MagicMock()
        mock_corner_1_lon.__float__.return_value = 1.0

        mock_corner_2_lat = MagicMock()
        mock_corner_2_lat.__float__.return_value = 1.0

        mock_corner_2_lon = MagicMock()
        mock_corner_2_lon.__float__.return_value = 3.0

        under_test_1, under_test_2 = \
            convert_octagon_section_corners_coordinates_to_string(float(mock_corner_1_lat), float(mock_corner_1_lon),
                                                                  float(mock_corner_2_lat), float(mock_corner_2_lon))

        self.assertEqual(under_test_1, '3°0\'0.000"N, 1°0\'0.000"E')
        self.assertEqual(under_test_2, '1°0\'0.000"N, 3°0\'0.000"E')

    @mock.patch('LatLon23.Latitude')
    def test_convert_coordinate_to_degrees_and_minutes_string_with_latitude_should_return_latitude_string(self,
                                                                                                          mock_lat):
        mock_lat.to_string.side_effect = ['45', '30', '31.997', 'N']

        under_test = convert_coordinate_to_degrees_and_minutes_string(mock_lat)

        self.assertEqual(under_test, '45°30\'31.997"N')
        mock_lat.to_string.assert_called()
        self.assertEqual(mock_lat.to_string.call_count, 4)

    @mock.patch('LatLon23.Longitude')
    def test_convert_coordinate_to_degrees_and_minutes_string_with_longitude_should_return_longitude_string(self,
                                                                                                            mock_lon):
        mock_lon.to_string.side_effect = ['73', '33', '42.005', 'W']

        under_test = convert_coordinate_to_degrees_and_minutes_string(mock_lon)

        self.assertEqual(under_test, '73°33\'42.005"W')
        mock_lon.to_string.assert_called()
        self.assertEqual(mock_lon.to_string.call_count, 4)
