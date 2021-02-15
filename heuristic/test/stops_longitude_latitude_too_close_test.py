import unittest
from heuristic.stops_longitude_latitude_too_close import StopsLongitudeLatitudeTooClose


class StopsLongitudeLatitudeTooCloseTest(unittest.TestCase):
    def test_none_stop1_should_return_none(self):
        stop_1 = None
        stop_2 = {"stop_lat": 45.508888, "stop_lon": -73.561668}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertIsNone(under_test.execute(stop_1, stop_2))

    def test_none_stop2_should_return_none(self):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = None

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertIsNone(under_test.execute(stop_1, stop_2))

    def test_stops_closer_than_default_5_meters_with_same_latitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508888, "stop_lon": -73.561669}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2))

    def test_stops_farther_than_default_5_meters_with_same_latitude_should_return_false(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508888, "stop_lon": -73.561733}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2))

    def test_stops_closer_than_default_5_meters_with_same_longitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508889, "stop_lon": -73.561668}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2))

    def test_stops_farther_than_default_5_meters_with_same_longitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508933, "stop_lon": -73.561668}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2))

    def test_stops_closer_than_default_5_meters_should_return_true(self):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508889, "stop_lon": -73.561669}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2))

    def test_stops_farther_than_default_5_meters_should_return_true(self):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508933, "stop_lon": -73.561733}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2))

    def test_stops_closer_than_custom_threshold_with_same_latitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508888, "stop_lon": -73.561669}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2, 10))

    def test_stops_farther_than_custom_threshold_with_same_latitude_should_return_false(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508888, "stop_lon": -73.561798}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2, 10))

    def test_stops_closer_than_custom_threshold_with_same_longitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508889, "stop_lon": -73.561668}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2, 10))

    def test_stops_farther_than_custom_threshold_with_same_longitude_should_return_true(
        self,
    ):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508978, "stop_lon": -73.561668}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2, 10))

    def test_stops_closer_than_custom_threshold_should_return_true(self):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508889, "stop_lon": -73.561669}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertTrue(under_test.execute(stop_1, stop_2, 10))

    def test_stops_farther_than_custom_threshold_should_return_true(self):
        stop_1 = {"stop_lat": 45.508888, "stop_lon": -73.561668}
        stop_2 = {"stop_lat": 45.508978, "stop_lon": -73.561798}

        under_test = StopsLongitudeLatitudeTooClose()
        self.assertFalse(under_test.execute(stop_1, stop_2, 10))


if __name__ == "__main__":
    unittest.main()
