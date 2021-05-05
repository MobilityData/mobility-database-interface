import operator
from datetime import datetime, time, timedelta
import pytz
import pandas as pd

# Setting constants
SECONDS_PER_HOUR = 3600
MINUTES_PER_HOUR = 60
UTC_THRESHOLD = 12
START_DATE = "start_date"
END_DATE = "end_date"
DATE = "date"
SERVICE_ID = "service_id"
EXCEPTION_TYPE = "exception_type"
WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
DATE_FORMAT = "%Y%m%d"
TRIP_ID = "trip_id"


def get_gtfs_dates_by_type(dataset, date_type):
    # Initialize dataframe for the dataset dates
    dates_per_service_id_dataframe = pd.DataFrame(columns=[SERVICE_ID, DATE])

    # Add the dates from the dataset calendar to the dataframe
    if dataset.calendar is not None:
        if date_type == START_DATE:
            dates_per_service_id_dataframe = get_gtfs_start_dates_from_calendar(
                dataset.calendar, dates_per_service_id_dataframe
            )
        elif date_type == END_DATE:
            dates_per_service_id_dataframe = get_gtfs_end_dates_from_calendar(
                dataset.calendar, dates_per_service_id_dataframe
            )

    # Verify exceptions from dataset calendar dates
    if dataset.calendar_dates is not None:
        for index, row in dataset.calendar_dates.iterrows():
            date_index = dates_per_service_id_dataframe.loc[
                (dates_per_service_id_dataframe[SERVICE_ID] == row[SERVICE_ID])
                & (dates_per_service_id_dataframe[DATE] == row[DATE])
            ].index

            # Add a date if exception_type is 1
            # and if the date is not in the dataframe
            if row[EXCEPTION_TYPE] == 1 and len(date_index) == 0:
                service_id = row[SERVICE_ID]
                date = row[DATE]
                date_loc = service_id + "_" + date
                dates_per_service_id_dataframe.loc[date_loc] = [service_id] + [date]

            # Remove a date if exception_type is 2
            # and if the date is in the dataframe
            elif row[EXCEPTION_TYPE] == 2 and len(date_index) > 0:
                dates_per_service_id_dataframe.drop(list(date_index), inplace=True)

    return dates_per_service_id_dataframe


def get_gtfs_dates_from_calendar(
    start_or_end_date_key, dataset_calendar, dates_per_service_id_dataframe
):
    for index, row in dataset_calendar.iterrows():
        row_date_as_datetime = datetime.strptime(
            row[start_or_end_date_key], DATE_FORMAT
        )
        date_day_as_int = int(row_date_as_datetime.strftime("%w"))
        if start_or_end_date_key == START_DATE:
            timedelta_operator = operator.add
            # Compute the number of days to reach next monday
            day_offset_to_monday = abs((date_day_as_int - 1) % -7)
        elif start_or_end_date_key == END_DATE:
            timedelta_operator = operator.sub
            # Compute the number of days to reach previous monday
            day_offset_to_monday = (date_day_as_int - 1) % 7
        else:
            raise Exception(
                "Invalid value for start_or_end_date_key, must be 'start_date' or 'end_date"
            )

        # if start_date
        # Iterate in the calendar days to get the days of a service and adds it to the dataset_dates.
        # Consider the offset to next monday. Ex. If a service starts on tuesday,
        # then the first monday of the service will be start date + 6 days.
        # if end_date
        # Iterate in the calendar days to get the days of a service and adds it to the dataset_dates.
        # Consider the offset to next monday. Ex. If a service starts on sunday,
        # then the last monday of the service will be end date - 6 days.
        for day in WEEKDAYS:
            if row[day] == 1:
                service_id = row[SERVICE_ID]
                date_as_datetime = timedelta_operator(
                    row_date_as_datetime, timedelta(days=day_offset_to_monday)
                )
                date_as_string = date_as_datetime.strftime(DATE_FORMAT)
                date_loc = service_id + "_" + date_as_string
                dates_per_service_id_dataframe.loc[date_loc] = [service_id] + [
                    date_as_string
                ]
            day_offset_to_monday = timedelta_operator(day_offset_to_monday, 1) % 7

    # Make sure service_id and date are present for each row of the dataframe before returning it
    dates_per_service_id_dataframe = dates_per_service_id_dataframe.loc[
        dates_per_service_id_dataframe[SERVICE_ID].notna()
        & dates_per_service_id_dataframe[DATE].notna()
    ]

    return dates_per_service_id_dataframe


def get_gtfs_start_dates_from_calendar(
    dataset_calendar, dates_per_service_id_dataframe
):
    dates_per_service_id_dataframe = get_gtfs_dates_from_calendar(
        START_DATE, dataset_calendar, dates_per_service_id_dataframe
    )
    return dates_per_service_id_dataframe


def get_gtfs_end_dates_from_calendar(dataset_calendar, dates_per_service_id_dataframe):
    dates_per_service_id_dataframe = get_gtfs_dates_from_calendar(
        END_DATE, dataset_calendar, dates_per_service_id_dataframe
    )
    return dates_per_service_id_dataframe


def get_gtfs_timezone_utc_offset(dataset):
    # Extract agency timezone from dataset
    agency_timezone = dataset.agency["agency_timezone"].iloc[0]

    # Default timezone UTC offset is the empty string.
    # If the timezone is not recognized by pytz, then this value will be returned.
    timezone_offset = ""

    if agency_timezone in pytz.all_timezones:
        timezone = pytz.timezone(agency_timezone)

        # Compute the utc offset time and sign
        utc = datetime.utcnow()
        offset_seconds = timezone.utcoffset(utc).seconds
        if offset_seconds != 0:
            # compute offset in hour if offset is not equal to zero
            offset_hours = offset_seconds / SECONDS_PER_HOUR
            offset_sign = "+"
            if offset_hours > UTC_THRESHOLD:
                offset_hours = -1 * (offset_hours % -UTC_THRESHOLD)
                offset_sign = "-"
            offset_time_string = str(
                time(int(offset_hours), int((offset_hours % 1) * MINUTES_PER_HOUR))
            )

            # Keep the hour and minutes from the computed offset and add the offset sign to the string
            offset_hours_and_minutes = offset_time_string[0:5]
            timezone_offset = offset_sign + offset_hours_and_minutes
        else:
            # Set timezone offset to "±00:00" if offset is equal to zero
            timezone_offset = "±00:00"

    return timezone_offset


def get_gtfs_stop_times_for_date(
    dataset, dataset_dates, date_to_look_up, arrival_or_departure_time_key
):
    # Extract the list of every service ID with date equal to the date to look up
    service_dates = dataset_dates.loc[
        dataset_dates[DATE] == date_to_look_up.strftime(DATE_FORMAT)
    ]
    service_dates = service_dates.loc[service_dates[SERVICE_ID].notna()]
    service_ids_for_date = service_dates[SERVICE_ID].tolist()

    # Extract the list of every trip ID with service ID in the list of service IDs previously extracted
    trips_for_date = dataset.trips.loc[
        dataset.trips[SERVICE_ID].isin(service_ids_for_date)
    ]
    trips_for_date = trips_for_date.loc[trips_for_date[TRIP_ID].notna()]
    trip_ids_for_date = trips_for_date[TRIP_ID].tolist()

    # Extract the stop times with trip ID in the list of trip IDs previously extracted
    stop_times_for_date = dataset.stop_times.loc[
        dataset.stop_times[TRIP_ID].isin(trip_ids_for_date)
    ]
    stop_times_for_date = stop_times_for_date.loc[
        stop_times_for_date[arrival_or_departure_time_key].notna()
    ]
    return stop_times_for_date
