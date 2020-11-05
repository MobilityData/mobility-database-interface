import pandas as pd
import datetime
import pytz
from representation.gtfs_representation import GtfsRepresentation


class ProcessStartTimestampForGtfsMetadata:
    SECONDS_PER_HOUR = 3600
    UTC_THRESHOLD = 12

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
        """Execute the ``ProcessStartTimestampForGtfsMetadata`` use case.
        :return: The representation of the GTFS dataset post-execution.
        """
        # Extract the calendar start dates in the dataset representation
        dataset_calendar = self.gtfs_representation.get_dataset().calendar
        dataset_calendar['start_date'] = pd.to_datetime(dataset_calendar['start_date'], format='%Y%m%d')
        calendar_start_dates = dataset_calendar['start_date']

        # Get first start service date with min()
        start_service_date = calendar_start_dates.min()

        # Extract the list of every service ID with start date equal to start service date
        dataset_calendar = dataset_calendar.loc[dataset_calendar['start_date'] == start_service_date]
        service_ids = dataset_calendar['service_id'].tolist()

        # Extract the list of every trip ID with service ID in the list of service IDs previously extracted
        dataset_trips = self.gtfs_representation.get_dataset().trips
        dataset_trips = dataset_trips.loc[dataset_trips['service_id'].isin(service_ids)]
        trip_ids = dataset_trips['trip_id'].tolist()

        # Extract the stop times arrival times with trip ID in the list of trip IDs previously extracted
        dataset_stop_times = self.gtfs_representation.get_dataset().stop_times
        dataset_stop_times = dataset_stop_times.loc[dataset_stop_times['trip_id'].isin(trip_ids)]
        stop_arrival_times = dataset_stop_times['arrival_time']

        # Get first arrival time of the first start service date with min()
        first_stop_arrival_time = stop_arrival_times.min()

        # Extract the agency main timezone from the dataset representation
        dataset_agency = self.gtfs_representation.get_dataset().agency
        agency_main_timezone = dataset_agency['agency_timezone'].iloc[0]

        # Compute UTC offset
        timezone = pytz.timezone(agency_main_timezone)
        utc = datetime.datetime.utcnow()
        offset_seconds = timezone.utcoffset(utc).seconds
        offset_hours = offset_seconds / self.SECONDS_PER_HOUR
        offset_sign = "+"
        if offset_hours > self.UTC_THRESHOLD:
            offset_hours = -1 * (offset_hours % -self.UTC_THRESHOLD)
            offset_sign = "-"
        offset_time_string = str(datetime.time(int(offset_hours), int((offset_hours % 1) * 60)))
        offset_hours_and_minutes = offset_time_string[0:5]
        timezone_offset = offset_sign + offset_hours_and_minutes

        # Build timestamp string in ISO 8601 YYYY-MM-DDThh:mm:ss±hh:mm format
        start_timestamp = start_service_date.strftime('%Y-%m-%d') + "T" + first_stop_arrival_time + timezone_offset
        self.gtfs_representation.set_metadata_start_timestamp(start_timestamp)

        return self.gtfs_representation
