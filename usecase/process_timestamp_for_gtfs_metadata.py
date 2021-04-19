import pandas as pd
from utilities.validators import validate_gtfs_representation
from utilities.temporal_utils import (
    get_gtfs_dates_by_type,
    get_gtfs_timezone_utc_offset,
    get_gtfs_stop_times_for_date,
)
from utilities.constants import (
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY,
    DATE,
    SERVICE_ID,
    EXCEPTION_TYPE,
    TRIP_ID,
    AGENCY_TIMEZONE,
)


PD_DATE_FORMAT = "%Y%m%d"
TIMESTAMP_FORMAT = "%Y-%m-%d"
DATE_KEY = "date"

DATASET_DATE_TYPE = "dataset_date_type"
STOP_TIME_KEY = "stop_time_key"
MIN_MAX_ATTR = "min_max_attr"
TIMESTAMP_ATTR = "timestamp_setter"
CALENDAR_DATE_KEY = "calendar_date_key"

START_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: "start_date",
    STOP_TIME_KEY: "arrival_time",
    MIN_MAX_ATTR: "min",
    TIMESTAMP_ATTR: "start_timestamp",
    CALENDAR_DATE_KEY: "start_date",
}

END_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: "end_date",
    STOP_TIME_KEY: "departure_time",
    MIN_MAX_ATTR: "max",
    TIMESTAMP_ATTR: "end_timestamp",
    CALENDAR_DATE_KEY: "end_date",
}

CALENDAR_DATES_NECESSARY_COLUMNS = {
    DATE,
    SERVICE_ID,
    EXCEPTION_TYPE,
}

CALENDAR_NECESSARY_COLUMNS = {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY,
    SERVICE_ID,
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

    calendar_is_present = (
        dataset.calendar is not None
        and CALENDAR_NECESSARY_COLUMNS.union(
            {timestamp_map[CALENDAR_DATE_KEY]}
        ).issubset(dataset.calendar.columns)
    )
    calendar_dates_are_present = (
        dataset.calendar_dates is not None
        and CALENDAR_DATES_NECESSARY_COLUMNS.issubset(dataset.calendar_dates.columns)
    )
    trips_are_present = (
        dataset.trips is not None and SERVICE_ID in dataset.trips.columns
    )
    stop_times_are_present = dataset.stop_times is not None and (
        {TRIP_ID, timestamp_map[STOP_TIME_KEY]}
    ).issubset(dataset.stop_times.columns)
    agency_is_present = (
        dataset.agency is not None and AGENCY_TIMEZONE in dataset.agency.columns
    )

    if (
        (calendar_is_present)
        or (calendar_dates_are_present)
        and (trips_are_present)
        and (stop_times_are_present)
        and (agency_is_present)
    ):
        # Extract the start dates in the dataset representation
        # or
        # Extract the end dates in the dataset representation
        dataset_dates = get_gtfs_dates_by_type(
            dataset, date_type=timestamp_map[DATASET_DATE_TYPE]
        )
        dates = pd.to_datetime(dataset_dates[DATE_KEY], format=PD_DATE_FORMAT)

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
            stop_times_for_date[timestamp_map[STOP_TIME_KEY]],
            timestamp_map[MIN_MAX_ATTR],
        )()

        # Compute UTC offset for the GTFS dataset
        timezone_offset = get_gtfs_timezone_utc_offset(dataset)

        # Build timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
        timestamp = (
            f"{service_date.strftime(TIMESTAMP_FORMAT)}T{stop_time}{timezone_offset}"
        )
    else:
        timestamp = ""

    # Set timestamp
    setattr(metadata, timestamp_map[TIMESTAMP_ATTR], timestamp)

    return gtfs_representation
