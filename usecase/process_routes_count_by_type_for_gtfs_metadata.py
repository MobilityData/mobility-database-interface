from representation.gtfs_representation import GtfsRepresentation

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
ROUTE_TYPE = 'route_type'


def process_routes_count_by_type_for_gtfs_metadata(gtfs_representation):
    """Process and count by type all the routes in the `routes` file from the GTFS dataset of the representation.
    Add the dictionary of the routes count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")

    dataset = gtfs_representation.get_dataset()

    # Count routes by route type
    trams_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == TRAM].size
    subways_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == SUBWAY].size
    rails_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == RAIL].size
    buses_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == BUS].size
    ferries_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FERRY].size
    cable_trams_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == CABLE_TRAM].size
    aerial_lifts_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == AERIAL_LIFT].size
    funiculars_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FUNICULAR].size
    trolley_buses_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == TROLLEY_BUS].size
    monorails_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == MONORAIL].size

    # Create the dictionary of routes count by type
    routes_count_by_type = {'tram': trams_count, 'subway': subways_count,
                            'rail': rails_count, 'bus': buses_count,
                            'ferry': ferries_count, 'cable_tram': cable_trams_count,
                            'aerial_lift': aerial_lifts_count, 'funicular': funiculars_count,
                            'trolley_bus': trolley_buses_count, 'monorail': monorails_count}

    gtfs_representation.set_metadata_routes_count_by_type(routes_count_by_type)
    return gtfs_representation
