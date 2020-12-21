from representation.gtfs_representation import GtfsRepresentation


class ProcessStopsCountByTypeForGtfsMetadata:
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

        # Count stops by location type
        stops_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == 0].size
        stations_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == 1].size
        entrances_count = dataset.stops['location_type'].loc[dataset.stops['location_type'] == 2].size

        # Create the dictionary of stops count by type
        stops_count_by_type = {'stop': str(stops_count),
                               'station': str(stations_count),
                               'entrance': str(entrances_count)}

        self.gtfs_representation.set_metadata_stops_count_by_type(stops_count_by_type)
        return self.gtfs_representation
