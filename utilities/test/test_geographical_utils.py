import pandas as pd
from unittest import TestCase, mock
from unittest.mock import PropertyMock, MagicMock
from gtfs_kit.feed import Feed
from LatLon23 import Latitude, Longitude
from utilities.geographical_utils import *


class TestGeographicalUtils(TestCase):
    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_bounding_box_corner_strings_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_LAT: [45.508888, 44.508888], STOP_LON: [-73.561668, -74.561668]}
            )
        )
        type(mock_dataset).stops = mock_stops

        (
            under_test_1,
            under_test_2,
            under_test_3,
            under_test_4,
        ) = process_bounding_box_corner_strings(mock_dataset)

        self.assertEqual(under_test_1, "44°30'31.997\"N, 73°33'42.005\"W")
        self.assertEqual(under_test_2, "44°30'31.997\"N, 74°33'42.005\"W")
        self.assertEqual(under_test_3, "45°30'31.997\"N, 74°33'42.005\"W")
        self.assertEqual(under_test_4, "45°30'31.997\"N, 73°33'42.005\"W")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_bounding_octagon_corner_strings_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        type(mock_dataset).stops = mock_stops

        under_test = process_bounding_octagon_corner_strings(mock_dataset)
        under_test_1 = under_test[0]
        under_test_2 = under_test[1]
        under_test_3 = under_test[2]
        under_test_4 = under_test[3]
        under_test_5 = under_test[4]
        under_test_6 = under_test[5]
        under_test_7 = under_test[6]
        under_test_8 = under_test[7]

        self.assertEqual(under_test_1, "1°0'0.000\"S, 3°0'0.000\"E")
        self.assertEqual(under_test_2, "3°0'0.000\"S, 1°0'0.000\"E")
        self.assertEqual(under_test_3, "3°0'0.000\"S, 1°0'0.000\"W")
        self.assertEqual(under_test_4, "1°0'0.000\"S, 3°0'0.000\"W")
        self.assertEqual(under_test_5, "1°0'0.000\"N, 3°0'0.000\"W")
        self.assertEqual(under_test_6, "3°0'0.000\"N, 1°0'0.000\"W")
        self.assertEqual(under_test_7, "3°0'0.000\"N, 1°0'0.000\"E")
        self.assertEqual(under_test_8, "1°0'0.000\"N, 3°0'0.000\"E")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 5)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_geographical_coordinates_as_string_should_return_coordinates_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_LAT: [45.508888, 44.508888], STOP_LON: [-73.561668, -74.561668]}
            )
        )
        type(mock_dataset).stops = mock_stops

        (
            under_test_1,
            under_test_2,
            under_test_3,
            under_test_4,
        ) = process_geographical_coordinates_as_string(mock_dataset.stops)

        self.assertEqual(under_test_1, "45°30'31.997\"N")
        self.assertEqual(under_test_2, "44°30'31.997\"N")
        self.assertEqual(under_test_3, "73°33'42.005\"W")
        self.assertEqual(under_test_4, "74°33'42.005\"W")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_extract_geographical_coordinates_as_float_should_return_coordinates_as_float(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_LAT: [45.508888, 44.508888], STOP_LON: [-73.561668, -74.561668]}
            )
        )
        type(mock_dataset).stops = mock_stops

        (
            under_test_1,
            under_test_2,
            under_test_3,
            under_test_4,
        ) = extract_geographical_coordinates_as_float(mock_dataset.stops)

        self.assertEqual(under_test_1, 45.508888)
        self.assertEqual(under_test_2, 44.508888)
        self.assertEqual(under_test_3, -73.561668)
        self.assertEqual(under_test_4, -74.561668)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_upper_right_octagon_local_corners_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = process_octagon_local_corners(
            mock_dataset.stops, 3, 3, OCTAGON_UPPER_RIGHT_CORNER_MAP
        )

        self.assertEqual(under_test_1, "3°0'0.000\"N, 1°0'0.000\"E")
        self.assertEqual(under_test_2, "1°0'0.000\"N, 3°0'0.000\"E")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_lower_right_octagon_local_corners_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = process_octagon_local_corners(
            mock_dataset.stops, -3, 3, OCTAGON_LOWER_RIGHT_CORNER_MAP
        )

        self.assertEqual(under_test_1, "3°0'0.000\"S, 1°0'0.000\"E")
        self.assertEqual(under_test_2, "1°0'0.000\"S, 3°0'0.000\"E")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_lower_left_octagon_local_corners_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = process_octagon_local_corners(
            mock_dataset.stops, -3, -3, OCTAGON_LOWER_LEFT_CORNER_MAP
        )

        self.assertEqual(under_test_1, "3°0'0.000\"S, 1°0'0.000\"W")
        self.assertEqual(under_test_2, "1°0'0.000\"S, 3°0'0.000\"W")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    @mock.patch("gtfs_kit.feed.Feed")
    def test_process_upper_left_octagon_local_corners_should_return_corners_as_string(
        self, mock_dataset
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {
                    STOP_LAT: [3, -3, 0, 0, 2, -2, 2, -2],
                    STOP_LON: [0, 0, 3, -3, 2, 2, -2, -2],
                }
            )
        )
        type(mock_dataset).stops = mock_stops

        under_test_1, under_test_2 = process_octagon_local_corners(
            mock_dataset.stops, 3, -3, OCTAGON_UPPER_LEFT_CORNER_MAP
        )

        self.assertEqual(under_test_1, "3°0'0.000\"N, 1°0'0.000\"W")
        self.assertEqual(under_test_2, "1°0'0.000\"N, 3°0'0.000\"W")
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)

    def test_convert_geographical_coordinates_to_box_corner_strings_should_return_corners_string(
        self,
    ):
        mock_max_lat = MagicMock()
        mock_max_lat.__str__.return_value = "45°30'31.997\"N"

        mock_min_lat = MagicMock()
        mock_min_lat.__str__.return_value = "44°30'31.997\"N"

        mock_max_lon = MagicMock()
        mock_max_lon.__str__.return_value = "73°33'42.005\"W"

        mock_min_lon = MagicMock()
        mock_min_lon.__str__.return_value = "74°33'42.005\"W"

        (
            under_test_1,
            under_test_2,
            under_test_3,
            under_test_4,
        ) = convert_geographical_coordinates_to_box_corner_strings(
            str(mock_max_lat), str(mock_min_lat), str(mock_max_lon), str(mock_min_lon)
        )

        self.assertEqual(under_test_1, "44°30'31.997\"N, 73°33'42.005\"W")
        self.assertEqual(under_test_2, "44°30'31.997\"N, 74°33'42.005\"W")
        self.assertEqual(under_test_3, "45°30'31.997\"N, 74°33'42.005\"W")
        self.assertEqual(under_test_4, "45°30'31.997\"N, 73°33'42.005\"W")

    def test_convert_octagon_section_corners_coordinates_to_corner_strings_should_return_corners_string(
        self,
    ):
        mock_corner_1_lat = MagicMock()
        mock_corner_1_lat.__float__.return_value = 3.0

        mock_corner_1_lon = MagicMock()
        mock_corner_1_lon.__float__.return_value = 1.0

        mock_corner_2_lat = MagicMock()
        mock_corner_2_lat.__float__.return_value = 1.0

        mock_corner_2_lon = MagicMock()
        mock_corner_2_lon.__float__.return_value = 3.0

        (
            under_test_1,
            under_test_2,
        ) = convert_octagon_section_corners_coordinates_to_corner_strings(
            float(mock_corner_1_lat),
            float(mock_corner_1_lon),
            float(mock_corner_2_lat),
            float(mock_corner_2_lon),
        )

        self.assertEqual(under_test_1, "3°0'0.000\"N, 1°0'0.000\"E")
        self.assertEqual(under_test_2, "1°0'0.000\"N, 3°0'0.000\"E")

    def test_convert_coordinate_to_degrees_and_minutes_string_with_latitude_should_return_latitude_string(
        self,
    ):
        mock_lat = MagicMock()
        mock_lat.__float__.return_value = 45.508888

        under_test = convert_coordinate_to_degrees_and_minutes_string(
            Latitude, float(mock_lat)
        )
        self.assertEqual(under_test, "45°30'31.997\"N")

    def test_convert_coordinate_to_degrees_and_minutes_string_with_longitude_should_return_longitude_string(
        self,
    ):
        mock_lon = MagicMock()
        mock_lon.__float__.return_value = -73.561668

        under_test = convert_coordinate_to_degrees_and_minutes_string(
            Longitude, float(mock_lon)
        )
        self.assertEqual(under_test, "73°33'42.005\"W")
