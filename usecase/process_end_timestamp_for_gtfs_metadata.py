import pandas as pd

from utilities.temporal_utils import get_gtfs_dates_by_type, get_gtfs_timezone_utc_offset, get_gtfs_stop_times_for_date
from utilities.validators import validate_gtfs_representation


class ProcessEndTimestampForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessEndTimestampForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        validate_gtfs_representation(gtfs_representation)
        self.gtfs_representation = gtfs_representation

    def execute(self):
        """Execute the ``ProcessEndTimestampForGtfsMetadata`` use case. Process the end timestamp using the `agency`,
        `calendar`, `calendar_dates`, `trips` and `stop_times` files from the GTFS dataset of the representation.
        Add the end timestamp to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the end dates in the dataset representation
        dataset_dates = get_gtfs_dates_by_type(dataset, date_type='end_date')
        end_dates = pd.to_datetime(dataset_dates['date'], format='%Y%m%d')

        # Get last end service date with max()
        end_service_date = end_dates.max()

        # Get every stop time of the dataset for the end service date
        stop_times_for_date = get_gtfs_stop_times_for_date(dataset, dataset_dates, end_service_date)

        # Get last departure time of the last end service date with max()
        last_stop_departure_time = stop_times_for_date['departure_time'].max()

        # Compute UTC offset for the GTFS dataset
        timezone_offset = get_gtfs_timezone_utc_offset(dataset)

        # Build timestamp string in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
        end_timestamp = end_service_date.strftime('%Y-%m-%d') + "T" + last_stop_departure_time + timezone_offset
        self.gtfs_representation.set_metadata_end_timestamp(end_timestamp)

        return self.gtfs_representation
