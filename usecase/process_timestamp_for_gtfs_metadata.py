import pandas as pd
from utilities.validators import validate_gtfs_representation
from utilities.temporal_utils import (
    get_gtfs_dates_by_type,
    get_gtfs_timezone_utc_offset,
    get_gtfs_stop_times_for_date,
)
from utilities.notices import (
    STANDALONE,
    WITH_FILENAME,
    FILENAME,
    CALENDAR_TXT,
    CALENDAR_DATES_TXT,
    STOP_TIMES_TXT,
    TRIPS_TXT,
    AGENCY_TXT,
    MISSING_CALENDAR_AND_CALENDAR_DATE_FILES,
    BLOCK_TRIPS_WITH_OVERLAPPING_STOP_TIMES,
    STOP_TIME_WITH_ONLY_ARRIVAL_OR_DEPARTURE_TIME,
    STOP_TIME_WITH_ARRIVAL_BEFORE_PREVIOUS_DEPARTURE_TIME,
    MISSING_TRIP_EDGE,
    INCONSISTENT_AGENCY_TIMEZONE,
    DUPLICATED_COLUMN,
    DUPLICATE_KEY,
    EMPTY_FILE,
    INVALID_DATE,
    INVALID_ROW_LENGTH,
    INVALID_TIME,
    INVALID_TIMEZONE,
    LEADING_OR_TRAILING_WHITESPACES,
    MISSING_REQUIRED_COLUMN,
    MISSING_REQUIRED_FIELD,
    MISSING_REQUIRED_FILE,
    NEW_LINE_IN_VALUE,
    NUMBER_OUT_OF_RANGE,
    START_AND_END_RANGE_OUT_OF_ORDER,
    START_AND_END_RANGE_EQUAL,
    FOREIGN_KEY_VIOLATION,
    IO_ERROR,
    THREAD_EXECUTION_ERROR,
    THREAD_INTERRUPTED_ERROR,
    URI_SYNTAX_ERROR,
    RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
)

PD_DATE_FORMAT = "%Y%m%d"
TIMESTAMP_FORMAT = "%Y-%m-%d"
DATE = "date"

DATASET_DATE_TYPE = "dataset_date_type"
STOP_TIME_KEY = "stop_time_key"
MIN_MAX_ATTR = "min_max_attr"
TIMESTAMP_ATTR = "timestamp_setter"

START_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: "start_date",
    STOP_TIME_KEY: "arrival_time",
    MIN_MAX_ATTR: "min",
    TIMESTAMP_ATTR: "start_timestamp",
}

END_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: "end_date",
    STOP_TIME_KEY: "departure_time",
    MIN_MAX_ATTR: "max",
    TIMESTAMP_ATTR: "end_timestamp",
}

TIMESTAMP_NOTICES = {
    STANDALONE: {
        MISSING_CALENDAR_AND_CALENDAR_DATE_FILES,
        BLOCK_TRIPS_WITH_OVERLAPPING_STOP_TIMES,
        STOP_TIME_WITH_ONLY_ARRIVAL_OR_DEPARTURE_TIME,
        STOP_TIME_WITH_ARRIVAL_BEFORE_PREVIOUS_DEPARTURE_TIME,
        MISSING_TRIP_EDGE,
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
        INVALID_DATE,
        INVALID_ROW_LENGTH,
        INVALID_TIME,
        INVALID_TIMEZONE,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        START_AND_END_RANGE_OUT_OF_ORDER,
        START_AND_END_RANGE_EQUAL,
        FOREIGN_KEY_VIOLATION,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {CALENDAR_TXT, CALENDAR_DATES_TXT, STOP_TIMES_TXT, TRIPS_TXT, AGENCY_TXT},
}


def process_start_timestamp_for_gtfs_metadata(gtfs_representation):
    return process_timestamp_for_gtfs_metadata(gtfs_representation, START_TIMESTAMP_MAP)


def process_end_timestamp_for_gtfs_metadata(gtfs_representation):
    return process_timestamp_for_gtfs_metadata(gtfs_representation, END_TIMESTAMP_MAP)


def process_timestamp_for_gtfs_metadata(gtfs_representation, timestamp_map):
    """Process the start/end timestamp using the `agency`,
    `calendar`, `calendar_dates`, `trips` and `stop_times` files from the GTFS dataset
    of the representation, depending on which timestamp_map it receives.
    Add the end timestamp to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param timestamp_map: either START_TIMESTAMP_MAP or END_TIMESTAMP_MAP
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract the start dates in the dataset representation
    # or
    # Extract the end dates in the dataset representation
    dataset_dates = get_gtfs_dates_by_type(
        dataset, date_type=timestamp_map[DATASET_DATE_TYPE]
    )
    dates = pd.to_datetime(dataset_dates[DATE], format=PD_DATE_FORMAT)

    # Get first start service date with min()
    # or
    # Get last end service date with max()
    service_date = getattr(dates, timestamp_map[MIN_MAX_ATTR])()

    # Get every stop time of the dataset for the start service date
    # or
    # Get every stop time of the dataset for the end service date
    stop_times_for_date = get_gtfs_stop_times_for_date(
        dataset, dataset_dates, service_date
    )

    # Get first arrival time of the first start service date with min()
    # or
    # Get last departure time of the last end service date with max()
    stop_time = getattr(
        stop_times_for_date[timestamp_map[STOP_TIME_KEY]], timestamp_map[MIN_MAX_ATTR]
    )()

    # Compute UTC offset for the GTFS dataset
    timezone_offset = get_gtfs_timezone_utc_offset(dataset)

    # Build and set timestamp string in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
    timestamp = (
        f"{service_date.strftime(TIMESTAMP_FORMAT)}T{stop_time}{timezone_offset}"
    )
    setattr(metadata, timestamp_map[TIMESTAMP_ATTR], timestamp)

    return gtfs_representation
