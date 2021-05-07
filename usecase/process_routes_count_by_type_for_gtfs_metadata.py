import os
from utilities.validators import validate_gtfs_representation
from utilities.constants import (
    TRAM,
    SUBWAY,
    RAIL,
    BUS,
    FERRY,
    CABLE_TRAM,
    AERIAL_LIFT,
    FUNICULAR,
    TROLLEY_BUS,
    MONORAIL,
    ROUTE_TYPE,
    TRAM_CODE,
    SUBWAY_CODE,
    RAIL_CODE,
    BUS_CODE,
    FERRY_CODE,
    CABLE_TRAM_CODE,
    AERIAL_LIFT_CODE,
    FUNICULAR_CODE,
    TROLLEY_BUS_CODE,
    MONORAIL_CODE,
)

TRAM_KEY = "Tram"
SUBWAY_KEY = "Subway"
RAIL_KEY = "Rail"
BUS_KEY = "Bus"
FERRY_KEY = "Ferry"
CABLE_TRAM_KEY = "Cable tram"
AERIAL_LIFT_KEY = "Aerial lift"
FUNICULAR_KEY = "Funicular"
TROLLEY_BUS_KEY = "Trolleybus"
MONORAIL_KEY = "Monorail"


def process_routes_count_by_type_for_gtfs_metadata(gtfs_representation):
    """Process and count by type all the routes in the `routes` file from the GTFS dataset of the representation.
    Add the dictionary of the routes count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    routes_are_present = (
        dataset.routes is not None and ROUTE_TYPE in dataset.routes.columns
    )

    if routes_are_present:
        # Count routes by route type
        trams_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == TRAM].size
        )
        subways_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == SUBWAY].size
        )
        rails_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == RAIL].size
        )
        buses_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == BUS].size
        )
        ferries_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FERRY].size
        )
        cable_trams_count = (
            dataset.routes[ROUTE_TYPE]
            .loc[dataset.routes[ROUTE_TYPE] == CABLE_TRAM]
            .size
        )
        aerial_lifts_count = (
            dataset.routes[ROUTE_TYPE]
            .loc[dataset.routes[ROUTE_TYPE] == AERIAL_LIFT]
            .size
        )
        funiculars_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FUNICULAR].size
        )
        trolley_buses_count = (
            dataset.routes[ROUTE_TYPE]
            .loc[dataset.routes[ROUTE_TYPE] == TROLLEY_BUS]
            .size
        )
        monorails_count = (
            dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == MONORAIL].size
        )

        # Create the dictionary of routes count by type
        routes_count_by_type = {
            os.environ[TRAM_CODE]: trams_count,
            os.environ[SUBWAY_CODE]: subways_count,
            os.environ[RAIL_CODE]: rails_count,
            os.environ[BUS_CODE]: buses_count,
            os.environ[FERRY_CODE]: ferries_count,
            os.environ[CABLE_TRAM_CODE]: cable_trams_count,
            os.environ[AERIAL_LIFT_CODE]: aerial_lifts_count,
            os.environ[FUNICULAR_CODE]: funiculars_count,
            os.environ[TROLLEY_BUS_CODE]: trolley_buses_count,
            os.environ[MONORAIL_CODE]: monorails_count,
        }

        # Clean the dictionary to keep only the route type
        # where the route count is one or more
        routes_count_by_type = {
            key: count for key, count in routes_count_by_type.items() if count > 0
        }

        # Set the routes count by type in the GTFS representation
        # if the dictionary is not empty
        if len(routes_count_by_type) != 0:
            metadata.routes_count_by_type = routes_count_by_type

    return gtfs_representation
