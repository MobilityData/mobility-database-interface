from geopy.distance import geodesic


class StopsLongitudeLatitudeTooClose:
    LATITUDE_DEGREE_IN_METER = 111319.5

    def execute(self, stop_1, stop_2, min_distance=5.0):
        # Computing latitude distance first as it is a constant.
        # According to Wikipedia, 1 degree of latitude is 111319.5 meters
        # https://en.wikipedia.org/wiki/Decimal_degrees
        latitude_distance = abs(stop_1["stop_lat"] - stop_2["stop_lat"]) * self.LATITUDE_DEGREE_IN_METER

        # If latitude distance is smaller than minimal distance, in meters, verify with longitude
        if latitude_distance > min_distance:
            return False
        else:
            geolocation_1 = (stop_1["stop_lat"], stop_1["stop_lon"])
            geolocation_2 = (stop_2["stop_lat"], stop_2["stop_lon"])
            distance = geodesic(geolocation_1, geolocation_2).meters
            return distance < min_distance
