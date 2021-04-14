from utilities.validators import validate_gtfs_representation
from utilities.notices import (
    INCONSISTENT_AGENCY_TIMEZONE,
    STATION_WITH_PARENT_STATION,
    LOCATION_WITHOUT_PARENT_STATION,
    WRONG_PARENT_LOCATION_TYPE,
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

STOP_TIMEZONE_KEY = "stop_timezone"
AGENCY_TIMEZONE_KEY = "agency_timezone"
AGENCY_TIMEZONE_IDX = 0

TIMEZONE_NOTICES = {
    "validation_errors_standalone": {
        INCONSISTENT_AGENCY_TIMEZONE,
        STATION_WITH_PARENT_STATION,
        LOCATION_WITHOUT_PARENT_STATION,
        WRONG_PARENT_LOCATION_TYPE,
    },
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
    "filename": {"agency.txt", "stops.txt"},
}


def process_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract main timezone
    main_timezone = dataset.agency[AGENCY_TIMEZONE_KEY].iloc[AGENCY_TIMEZONE_IDX]

    # Extract the timezones using the stop_timezone in the dataset stops
    stop_timezones = set()
    if STOP_TIMEZONE_KEY in dataset.stops.columns:
        for index, row in dataset.stops.iterrows():
            if row[STOP_TIMEZONE_KEY] is not None:
                stop_timezones.add(row[STOP_TIMEZONE_KEY])

    # Remove the main_timezone from the set of the stop_timezones
    # to create the other_timezones
    other_timezones = []
    if len(stop_timezones) != 0:
        other_timezones = stop_timezones
        other_timezones.discard(main_timezone)
        # Convert the set of time to a list, and sort it alphabetically
        other_timezones = sorted(list(other_timezones))

    # Set the timezones in the GTFS representation
    metadata.main_timezone = main_timezone
    metadata.other_timezones = other_timezones

    return gtfs_representation
