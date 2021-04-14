from utilities.validators import validate_gtfs_representation
from utilities.notices import (
    STANDALONE,
    WITH_FILENAME,
    FILENAME,
    AGENCY_TXT,
    STOPS_TXT,
    INCONSISTENT_AGENCY_TIMEZONE,
    DUPLICATED_COLUMN,
    DUPLICATE_KEY,
    EMPTY_FILE,
    INVALID_ROW_LENGTH,
    INVALID_TIMEZONE,
    LEADING_OR_TRAILING_WHITESPACES,
    MISSING_REQUIRED_COLUMN,
    MISSING_REQUIRED_FIELD,
    MISSING_REQUIRED_FILE,
    NEW_LINE_IN_VALUE,
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
    STANDALONE: {
        INCONSISTENT_AGENCY_TIMEZONE,
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_ROW_LENGTH,
        INVALID_TIMEZONE,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {AGENCY_TXT, STOPS_TXT},
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
