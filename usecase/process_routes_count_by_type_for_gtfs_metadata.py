from representation.gtfs_representation import GtfsRepresentation


class ProcessRoutesCountByTypeForGtfsMetadata:
    TRAM = 0
    SUBWAY = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    AERIAL_LIFT = 6
    FUNICULAR = 7
    TROLLEY_BUS = 11
    MONORAIL = 12

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
        trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.TRAM].size
        subways_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.SUBWAY].size
        rails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.RAIL].size
        buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.BUS].size
        ferries_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.FERRY].size
        cable_trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.CABLE_TRAM].size
        aerial_lifts_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.AERIAL_LIFT].size
        funiculars_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.FUNICULAR].size
        trolley_buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.TROLLEY_BUS].size
        monorails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == self.MONORAIL].size

        # Create the dictionary of routes count by type
        routes_count_by_type = {'tram': trams_count, 'subway': subways_count,
                                'rail': rails_count, 'bus': buses_count,
                                'ferry': ferries_count, 'cable_tram': cable_trams_count,
                                'aerial_lift': aerial_lifts_count, 'funicular': funiculars_count,
                                'trolley_bus': trolley_buses_count, 'monorail': monorails_count}

        self.gtfs_representation.set_metadata_routes_count_by_type(routes_count_by_type)
        return self.gtfs_representation
