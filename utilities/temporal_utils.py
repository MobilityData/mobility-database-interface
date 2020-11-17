from datetime import datetime, time, timedelta
import pytz
import pandas as pd

# Setting constants
SECONDS_PER_HOUR = 3600
MINUTES_PER_HOUR = 60
UTC_THRESHOLD = 12


def get_gtfs_dates_by_type(dataset, date_type):
    # Initialize dataframe for the dataset dates
    dates_dataframe = pd.DataFrame(columns=['service_id', 'date'])

    # Add the dates from the dataset calendar to the dataframe
    if dataset.calendar is not None:
        if date_type == 'start_date':
            dates_dataframe = get_gtfs_start_dates_from_calendar(dataset.calendar, dates_dataframe)
        elif date_type == 'end_date':
            dates_dataframe = get_gtfs_end_dates_from_calendar(dataset.calendar, dates_dataframe)

    # Verify exceptions from dataset calendar dates
    if dataset.calendar_dates is not None:
        for index, row in dataset.calendar_dates.iterrows():
            date_index = dates_dataframe.loc[(dates_dataframe['service_id'] == row['service_id']) &
                                             (dates_dataframe['date'] == row['date'])].index

            if row['exception_type'] == 1 and len(date_index) == 0:
                service_id = row['service_id']
                date = row['date']
                date_loc = service_id + '_' + date
                dates_dataframe.loc[date_loc] = [service_id] + [date]

            elif row['exception_type'] == 2 and len(date_index) > 0:
                dates_dataframe.drop(date_index)

    return dates_dataframe


def get_gtfs_start_dates_from_calendar(dataset_calendar, dates_dataframe):
    for index, row in dataset_calendar.iterrows():
        row_start_date_as_datetime = datetime.strptime(row['start_date'], '%Y%m%d')

        # Compute the number of days to reach next monday
        start_date_day_as_int = int(row_start_date_as_datetime.strftime("%w"))
        day_offset_to_monday = abs((start_date_day_as_int - 1) % -7)

        # Iterate in the calendar days to get the days of a service and adds it to the dataset_dates.
        # Consider the offset to next monday. Ex. If a service starts on tuesday,
        # than the first monday of the service will be start date + 6 days.
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            if row[day] == 1:
                service_id = row['service_id']
                date_as_datetime = row_start_date_as_datetime + timedelta(days=day_offset_to_monday)
                date_as_string = date_as_datetime.strftime('%Y%m%d')
                date_loc = service_id + '_' + date_as_string
                dates_dataframe.loc[date_loc] = [service_id] + [date_as_string]
            day_offset_to_monday = (day_offset_to_monday + 1) % 7

    return dates_dataframe


def get_gtfs_end_dates_from_calendar(dataset_calendar, dates_dataframe):
    for index, row in dataset_calendar.iterrows():
        row_end_date_as_datetime = datetime.strptime(row['end_date'], '%Y%m%d')

        # Compute the number of days to reach previous monday
        end_date_day_as_int = int(row_end_date_as_datetime.strftime("%w"))
        day_offset_to_monday = (end_date_day_as_int - 1) % 7

        # Iterate in the calendar days to get the days of a service and adds it to the dataset_dates.
        # Consider the offset to next monday. Ex. If a service starts on sunday,
        # than the last monday of the service will be end date - 6 days.
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            if row[day] == 1:
                service_id = row['service_id']
                date_as_datetime = row_end_date_as_datetime - timedelta(days=day_offset_to_monday)
                date_as_string = date_as_datetime.strftime('%Y%m%d')
                date_loc = service_id + '_' + date_as_string
                dates_dataframe.loc[date_loc] = [service_id] + [date_as_string]
            day_offset_to_monday = (day_offset_to_monday - 1) % 7

    return dates_dataframe


def get_gtfs_timezone_utc_offset(dataset):
    # Extract agency timezone from dataset
    agency_timezone = dataset.agency['agency_timezone'].iloc[0]
    timezone = pytz.timezone(agency_timezone)
    # TODO verify timezone is valid

    # Compute the utc offset time and sign
    utc = datetime.utcnow()
    offset_seconds = timezone.utcoffset(utc).seconds
    offset_hours = offset_seconds / SECONDS_PER_HOUR
    offset_sign = "+"
    if offset_hours > UTC_THRESHOLD:
        offset_hours = -1 * (offset_hours % -UTC_THRESHOLD)
        offset_sign = "-"
    offset_time_string = str(time(int(offset_hours), int((offset_hours % 1) * MINUTES_PER_HOUR)))

    # Keep the hour and minutes from the computed offset and add the offset sign to the string
    offset_hours_and_minutes = offset_time_string[0:5]
    timezone_offset = offset_sign + offset_hours_and_minutes

    return timezone_offset


def get_gtfs_stop_times_for_date(dataset, dataset_dates, date_to_look_up):
    # Extract the list of every service ID with date equal to the date to look up
    service_dates = dataset_dates.loc[dataset_dates['date'] == date_to_look_up.strftime('%Y%m%d')]
    service_ids_for_date = service_dates['service_id'].tolist()

    # Extract the list of every trip ID with service ID in the list of service IDs previously extracted
    trips_for_date = dataset.trips.loc[dataset.trips['service_id'].isin(service_ids_for_date)]
    trip_ids_for_date = trips_for_date['trip_id'].tolist()

    # Extract the stop times with trip ID in the list of trip IDs previously extracted
    stop_times_for_date = dataset.stop_times.loc[dataset.stop_times['trip_id'].isin(trip_ids_for_date)]
    return stop_times_for_date
