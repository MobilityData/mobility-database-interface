from heuristic.stops_longitude_latitude_too_close import StopsLongitudeLatitudeTooClose


class CompareGtfsStops:
    def __init__(self, gtfs_1, gtfs_2):
        """Constructor for ``CompareGtfsStops``.
        :param gtfs_1: First GTFS dataset for the comparison.
        :param gtfs_2: Second GTFS dataset for the comparison.
        """
        self.stops_1 = gtfs_1.get_stops()
        self.stops_2 = gtfs_2.get_stops()

    def execute(self):
        """Execute comparison between the two GTFS datasets."""
        stops_longitude_latitude_too_close = StopsLongitudeLatitudeTooClose()
        for i in range(len(self.stops_1)):
            for j in range(len(self.stops_2)):
                stops_longitude_latitude_too_close.execute(
                    self.stops_1.iloc[i], self.stops_2.iloc[j]
                )
