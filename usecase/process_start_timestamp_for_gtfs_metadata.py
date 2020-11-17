import pandas as pd
from representation.gtfs_representation import GtfsRepresentation
from utilities.temporal_utils import get_gtfs_dates_by_type, get_gtfs_timezone_utc_offset, get_gtfs_stop_times_for_date


class ProcessStartTimestampForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessStartTimestampForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessStartTimestampForGtfsMetadata`` use case. Process the start timestamp using the
        `agency`, `calendar`, `calendar_dates`, `trips` and `stop_times` files from the GTFS dataset of the
        representation. Add the start timestamp to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the start dates in the dataset representation
        dataset_dates = get_gtfs_dates_by_type(dataset, date_type='start_date')
        start_dates = pd.to_datetime(dataset_dates['date'], format='%Y%m%d')

        # Get first start service date with min()
        start_service_date = start_dates.min()

        # Get every stop time of the dataset for the start service date
        stop_times_for_date = get_gtfs_stop_times_for_date(dataset, dataset_dates, start_service_date)

        # Get first arrival time of the first start service date with min()
        first_stop_arrival_time = stop_times_for_date['arrival_time'].min()

        # Compute UTC offset for the GTFS dataset
        timezone_offset = get_gtfs_timezone_utc_offset(dataset)

        # Build timestamp string in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
        start_timestamp = start_service_date.strftime('%Y-%m-%d') + "T" + first_stop_arrival_time + timezone_offset
        self.gtfs_representation.set_metadata_start_timestamp(start_timestamp)

        return self.gtfs_representation
