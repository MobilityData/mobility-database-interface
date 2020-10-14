from geopy.distance import geodesic


class StopsLongitudeLatitudeTooClose:
    LATITUDE_DEGREE_IN_METER = 111319.5

    def execute(self, stop_1, stop_2, min_distance_meter=5.0):
        """Verifies if two stop are too close by comparing latitude and longitude.
        :param stop_1: First stop to compare.
        :param stop_2: Second stop to compare.
        :param min_distance_meter: Minimum distance threshold in meter. Default at 5m.
        :returns: `boolean`. True if the two stops are closer than the ``min_distance_meter``, false otherwise.
        """
        if stop_1 is not None and stop_2 is not None:
            # Computing latitude distance first as it is a constant.
            # According to Wikipedia, 1 degree of latitude is 111319.5 meters
            # https://en.wikipedia.org/wiki/Decimal_degrees
            latitude_distance = abs(stop_1["stop_lat"] - stop_2["stop_lat"]) * self.LATITUDE_DEGREE_IN_METER

            # If latitude distance is smaller than minimal distance, in meters, verify with longitude
            if latitude_distance > min_distance_meter:
                return False
            else:
                geolocation_1 = (stop_1["stop_lat"], stop_1["stop_lon"])
                geolocation_2 = (stop_2["stop_lat"], stop_2["stop_lon"])
                distance = geodesic(geolocation_1, geolocation_2).meters
                return distance < min_distance_meter
