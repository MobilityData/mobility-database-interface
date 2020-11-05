import pandas as pd
from representation.gtfs_representation import GtfsRepresentation


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
        """Execute the ``ProcessStartServiceDateForGtfsMetadata`` use case.
        :return: The representation of the GTFS dataset post-execution.
        """
        # Extract the calendar start dates in the dataset representation
        dataset_calendar = self.gtfs_representation.get_dataset().calendar
        calendar_start_dates = pd.to_datetime(dataset_calendar['start_date'], format='%Y%m%d')

        # Get first start service date with min() and converting the date into a ISO 8601 string
        start_service_date = calendar_start_dates.min().strftime('%Y-%m-%d')
        self.gtfs_representation.set_metadata_start_service_date(start_service_date)

        return self.gtfs_representation
