from representation.gtfs_representation import GtfsRepresentation


class ProcessStopsCountByTypeForGtfsMetadata:
    STOP = 0
    STATION = 1
    ENTRANCE = 2

    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessStopsCountByTypeForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessStopsCountByTypeForGtfsMetadata`` use case.
        Process and count by type all the stops in the `stops` file from the GTFS dataset of the representation.
        Add the dictionary of the stops count to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Transform the blank location types to 0
        # According to the GTFS specification, blank location type is a Stop
        dataset.stops['location_type'] = dataset.stops['location_type'].fillna(0)
        dataset.stops = dataset.stops

        # Count stops by location type
        stops_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == self.STOP].size
        stations_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == self.STATION].size
        entrances_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == self.ENTRANCE].size

        # Create the dictionary of stops count by type
        stops_count_by_type = {'stop': stops_count,
                               'station': stations_count,
                               'entrance': entrances_count}

        self.gtfs_representation.set_metadata_stops_count_by_type(stops_count_by_type)
        return self.gtfs_representation
