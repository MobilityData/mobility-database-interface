import pandas as pd
from representation.gtfs_representation import GtfsRepresentation
from utilities.temporal_utils import get_gtfs_dates_by_type


class ProcessStartServiceDateForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessStartServiceDateForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessStartServiceDateForGtfsMetadata`` use case. Process the start service date using the
        `feed_info`, `calendar` and `calendar_dates` files from the GTFS dataset of the representation.
        Add the start service date to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        if dataset.feed_info is not None and not dataset.feed_info['feed_start_date'].isnull().values.all():
            # Extract start service date from feed info if the file is provided and
            filtered_feed_info = dataset.feed_info.loc[dataset.feed_info['feed_start_date'].notnull()]
            start_dates = pd.to_datetime(filtered_feed_info['feed_start_date'], format='%Y%m%d')
        else:
            # Extract the start dates in the dataset representation
            dataset_dates = get_gtfs_dates_by_type(dataset, date_type='start_date')
            start_dates = pd.to_datetime(dataset_dates['date'], format='%Y%m%d')

        # Get first start service date with min() and converting the date into a ISO 8601 string
        start_service_date = start_dates.min().strftime('%Y-%m-%d')

        self.gtfs_representation.set_metadata_start_service_date(start_service_date)
        return self.gtfs_representation
