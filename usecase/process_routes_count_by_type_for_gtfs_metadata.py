from representation.gtfs_representation import GtfsRepresentation


class ProcessRoutesCountByTypeForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessRoutesCountByTypeForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessRoutesCountByTypeForGtfsMetadata`` use case.
        Process and count by type all the routes in the `routes` file from the GTFS dataset of the representation.
        Add the dictionary of the routes count to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Count routes by route type
        trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 0].size
        subways_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 1].size
        rails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 2].size
        buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 3].size
        ferries_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 4].size
        cable_trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 5].size
        aerial_lifts_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 6].size
        funiculars_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 7].size
        trolley_buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 11].size
        monorails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == 12].size

        # Create the dictionary of routes count by type
        routes_count_by_type = {'tram': str(trams_count), 'subway': str(subways_count),
                                'rail': str(rails_count), 'bus': str(buses_count),
                                'ferry': str(ferries_count), 'cable_tram': str(cable_trams_count),
                                'aerial_lift': str(aerial_lifts_count), 'funicular': str(funiculars_count),
                                'trolley_bus': str(trolley_buses_count), 'monorail': str(monorails_count)}

        self.gtfs_representation.set_metadata_routes_count_by_type(routes_count_by_type)
        return self.gtfs_representation
