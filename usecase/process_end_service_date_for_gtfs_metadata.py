import pandas as pd
from representation.gtfs_representation import GtfsRepresentation


class ProcessEndServiceDateForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessEndServiceDateForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessEndServiceDateForGtfsMetadata`` use case.
        :return: The representation of the GTFS dataset post-execution.
        """
        # Extract the calendar end dates in the dataset representation
        dataset_calendar = self.gtfs_representation.get_dataset().calendar
        calendar_end_dates = pd.to_datetime(dataset_calendar['end_date'], format='%Y%m%d')

        # Get last end service date with max() and converting the date into a ISO 8601 string
        end_service_date = calendar_end_dates.max().strftime('%Y-%m-%d')
        self.gtfs_representation.set_metadata_end_service_date(end_service_date)

        return self.gtfs_representation
