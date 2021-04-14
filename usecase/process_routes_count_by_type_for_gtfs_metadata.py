from utilities.validators import validate_gtfs_representation
from utilities.notices import (
    ROUTE_BOTH_SHORT_AND_LONG_NAME_MISSING,
    DUPLICATED_COLUMN,
    DUPLICATE_KEY,
    EMPTY_FILE,
    INVALID_COLOR,
    INVALID_CURRENCY,
    INVALID_DATE,
    INVALID_EMAIL,
    INVALID_FLOAT,
    INVALID_INTEGER,
    INVALID_LANGUAGE_CODE,
    INVALID_PHONE_NUMBER,
    INVALID_ROW_LENGTH,
    INVALID_TIME,
    INVALID_TIMEZONE,
    INVALID_URL,
    LEADING_OR_TRAILING_WHITESPACES,
    MISSING_REQUIRED_COLUMN,
    MISSING_REQUIRED_FIELD,
    MISSING_REQUIRED_FILE,
    NEW_LINE_IN_VALUE,
    NUMBER_OUT_OF_RANGE,
    START_AND_END_RANGE_OUT_OF_ORDER,
    START_AND_END_RANGE_EQUAL,
    SAME_NAME_AND_DESCRIPTION_FOR_ROUTE,
    IO_ERROR,
    THREAD_EXECUTION_ERROR,
    THREAD_INTERRUPTED_ERROR,
    URI_SYNTAX_ERROR,
    RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
)

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
ROUTE_TYPE = "route_type"

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

ROUTES_COUNT_NOTICES = {
    "validation_errors_standalone": {ROUTE_BOTH_SHORT_AND_LONG_NAME_MISSING},
    "validation_errors_with_filename": {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_COLOR,
        INVALID_CURRENCY,
        INVALID_DATE,
        INVALID_EMAIL,
        INVALID_FLOAT,
        INVALID_INTEGER,
        INVALID_LANGUAGE_CODE,
        INVALID_PHONE_NUMBER,
        INVALID_ROW_LENGTH,
        INVALID_TIME,
        INVALID_TIMEZONE,
        INVALID_URL,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        START_AND_END_RANGE_OUT_OF_ORDER,
        START_AND_END_RANGE_EQUAL,
        SAME_NAME_AND_DESCRIPTION_FOR_ROUTE,
    },
    "system_errors_standalone": {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
    },
    "system_errors_with_filename": {RUNTIME_EXCEPTION_IN_LOADER_ERROR},
    "system_errors_with_classname": {RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR},
    "filename": {"routes.txt"},
}


def process_routes_count_by_type_for_gtfs_metadata(gtfs_representation):
    """Process and count by type all the routes in the `routes` file from the GTFS dataset of the representation.
    Add the dictionary of the routes count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

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
    buses_count = dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == BUS].size
    ferries_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FERRY].size
    )
    cable_trams_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == CABLE_TRAM].size
    )
    aerial_lifts_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == AERIAL_LIFT].size
    )
    funiculars_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == FUNICULAR].size
    )
    trolley_buses_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == TROLLEY_BUS].size
    )
    monorails_count = (
        dataset.routes[ROUTE_TYPE].loc[dataset.routes[ROUTE_TYPE] == MONORAIL].size
    )

    # Create the dictionary of routes count by type
    routes_count_by_type = {
        TRAM_KEY: trams_count,
        SUBWAY_KEY: subways_count,
        RAIL_KEY: rails_count,
        BUS_KEY: buses_count,
        FERRY_KEY: ferries_count,
        CABLE_TRAM_KEY: cable_trams_count,
        AERIAL_LIFT_KEY: aerial_lifts_count,
        FUNICULAR_KEY: funiculars_count,
        TROLLEY_BUS_KEY: trolley_buses_count,
        MONORAIL_KEY: monorails_count,
    }

    metadata.routes_count_by_type = routes_count_by_type
    return gtfs_representation
