import pandas as pd
from utilities.validators import validate_gtfs_representation
from utilities.temporal_utils import get_gtfs_dates_by_type, get_gtfs_timezone_utc_offset, get_gtfs_stop_times_for_date

PD_DATE_FORMAT = '%Y%m%d'
TIMESTAMP_FORMAT = '%Y-%m-%d'
DATE = 'date'

DATASET_DATE_TYPE = 'dataset_date_type'
STOP_TIME_KEY = 'stop_time_key'
MIN_MAX_ATTR = 'min_max_attr'
TIMESTAMP_SETTER = 'timestamp_setter'

START_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: 'start_date',
    STOP_TIME_KEY: 'arrival_time',
    MIN_MAX_ATTR: 'min',
    TIMESTAMP_SETTER: 'set_metadata_start_timestamp'
}

END_TIMESTAMP_MAP = {
    DATASET_DATE_TYPE: 'end_date',
    STOP_TIME_KEY: 'departure_time',
    MIN_MAX_ATTR: 'max',
    TIMESTAMP_SETTER: 'set_metadata_end_timestamp'
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
    dataset = gtfs_representation.get_dataset()

    # Extract the start dates in the dataset representation
    # or
    # Extract the end dates in the dataset representation
    dataset_dates = get_gtfs_dates_by_type(dataset, date_type=timestamp_map[DATASET_DATE_TYPE])
    dates = pd.to_datetime(dataset_dates[DATE], format=PD_DATE_FORMAT)

    # Get first start service date with min()
    # or
    # Get last end service date with max()
    service_date = getattr(dates, timestamp_map[MIN_MAX_ATTR])()

    # Get every stop time of the dataset for the start service date
    # or
    # Get every stop time of the dataset for the end service date
    stop_times_for_date = get_gtfs_stop_times_for_date(dataset, dataset_dates, service_date)

    # Get first arrival time of the first start service date with min()
    # or
    # Get last departure time of the last end service date with max()
    stop_time = getattr(stop_times_for_date[timestamp_map[STOP_TIME_KEY]], timestamp_map[MIN_MAX_ATTR])()

    # Compute UTC offset for the GTFS dataset
    timezone_offset = get_gtfs_timezone_utc_offset(dataset)

    # Build and set timestamp string in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
    timestamp = service_date.strftime(TIMESTAMP_FORMAT) + "T" + stop_time + timezone_offset
    getattr(gtfs_representation, timestamp_map[TIMESTAMP_SETTER])(timestamp)

    return gtfs_representation
