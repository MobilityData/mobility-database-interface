import pandas as pd

from utilities.temporal_utils import get_gtfs_dates_by_type
from utilities.validators import validate_gtfs_representation

PD_DATE_FORMAT = "%Y%m%d"
SERVICE_DATE_FORMAT = "%Y-%m-%d"
DATE = "date"

DATASET_DATE_TYPE = "dataset_date_type"
FEED_DATE_KEY = "feed_date_type"
MIN_MAX_ATTR = "min_max_attr"
SERVICE_DATE_SETTER = "service_date_setter"

START_DATE_MAP = {
    DATASET_DATE_TYPE: "start_date",
    FEED_DATE_KEY: "feed_start_date",
    MIN_MAX_ATTR: "min",
    SERVICE_DATE_SETTER: "set_metadata_start_service_date",
}

END_DATE_MAP = {
    DATASET_DATE_TYPE: "end_date",
    FEED_DATE_KEY: "feed_end_date",
    MIN_MAX_ATTR: "max",
    SERVICE_DATE_SETTER: "set_metadata_end_service_date",
}


def process_start_service_date_for_gtfs_metadata(gtfs_representation):
    return process_service_date_for_gtfs_metadata(gtfs_representation, START_DATE_MAP)


def process_end_service_date_for_gtfs_metadata(gtfs_representation):
    return process_service_date_for_gtfs_metadata(gtfs_representation, END_DATE_MAP)


def process_service_date_for_gtfs_metadata(gtfs_representation, service_date_map):
    """Execute the ``ProcessStartServiceDateForGtfsMetadata`` or ``ProcessEndServiceDateForGtfsMetadata`` use case
    depending on which service_date it receives.
    Process the start service date using the `feed_info`, `calendar` and `calendar_dates` files
    from the GTFS dataset of the representation.
    Add the start service date to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param service_date_map: Either START_DATE_MAP or END_DATE_MAP.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.get_dataset()
    feed_info = dataset.feed_info

    if (
        feed_info is not None
        and not feed_info[service_date_map[FEED_DATE_KEY]].isnull().values.all()
    ):
        # Extract start service date from feed info if the file is provided
        # or
        # Extract end service date from feed info if the file is provided
        feed_dates = feed_info[service_date_map[FEED_DATE_KEY]]
        filtered_feed_info = feed_info.loc[feed_dates.notnull()]
        dates = pd.to_datetime(
            filtered_feed_info[service_date_map[FEED_DATE_KEY]],
            format=PD_DATE_FORMAT,
        )
    else:
        # Extract the start dates in the dataset representation
        # or
        # Extract the end dates in the dataset representation
        dataset_dates = get_gtfs_dates_by_type(
            dataset, date_type=service_date_map[DATASET_DATE_TYPE]
        )
        dates = pd.to_datetime(dataset_dates[DATE], format=PD_DATE_FORMAT)

    # Get first start service date with min() and converting the date into a ISO 8601 string
    # or
    # Get last end service date with max() and converting the date into a ISO 8601 string
    service_date = getattr(dates, service_date_map[MIN_MAX_ATTR])()
    service_date = service_date.strftime(SERVICE_DATE_FORMAT)

    # Set the start service date in the GTFS representation
    # or
    # Set the end service date in the GTFS representation
    getattr(gtfs_representation, service_date_map[SERVICE_DATE_SETTER])(service_date)

    return gtfs_representation
