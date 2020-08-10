from geopy.distance import geodesic


class StopsLongitudeLatitudeTooClose:
    MIN_DISTANCE = 5.0

    def execute(self, stop_1, stop_2):
        stops_too_close = False
        geolocation_1 = (stop_1["stop_lat"], stop_1["stop_lon"])
        geolocation_2 = (stop_2["stop_lat"], stop_2["stop_lon"])
        distance = geodesic(geolocation_1, geolocation_2).meters

        if distance < self.MIN_DISTANCE:
            stops_too_close = True

        return stops_too_close
