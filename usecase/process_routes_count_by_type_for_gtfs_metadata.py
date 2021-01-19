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

def process_routes_count_by_type_for_gtfs_metadata(gtfs_representation):
    """Execute the ``ProcessRoutesCountByTypeForGtfsMetadata`` use case.
    Process and count by type all the routes in the `routes` file from the GTFS dataset of the representation.
    Add the dictionary of the routes count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")

    dataset = gtfs_representation.get_dataset()

    # Count routes by route type
    trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == TRAM].size
    subways_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == SUBWAY].size
    rails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == RAIL].size
    buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == BUS].size
    ferries_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == FERRY].size
    cable_trams_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == CABLE_TRAM].size
    aerial_lifts_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == AERIAL_LIFT].size
    funiculars_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == FUNICULAR].size
    trolley_buses_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == TROLLEY_BUS].size
    monorails_count = dataset.routes['route_type'].loc[dataset.routes['route_type'] == MONORAIL].size

    # Create the dictionary of routes count by type
    routes_count_by_type = {'tram': trams_count, 'subway': subways_count,
                            'rail': rails_count, 'bus': buses_count,
                            'ferry': ferries_count, 'cable_tram': cable_trams_count,
                            'aerial_lift': aerial_lifts_count, 'funicular': funiculars_count,
                            'trolley_bus': trolley_buses_count, 'monorail': monorails_count}

    gtfs_representation.set_metadata_routes_count_by_type(routes_count_by_type)
    return gtfs_representation
