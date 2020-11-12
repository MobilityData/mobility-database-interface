from datetime import datetime
import pandas as pd


def get_gtfs_start_dates_dataframe(dataset):
    dates_dataframe = pd.DataFrame(columns=['service_id', 'date'])
    if dataset.calendar is not None:
        for index, row in dataset.calendar.iterrows():
            # Compute the number of days to reach next monday
            start_date_day_as_int = int(datetime.strptime(row['start_date'], '%Y%m%d').strftime("%w"))
            day_offset_to_monday = abs((start_date_day_as_int - 1) % -7)

            # Iterate in the calendar days to get the days of a service and adds it to the dataset_dates.
            # Consider the offset to next monday. Ex. If a service starts on tuesday,
            # than the first monday of the service will be start date + 6 days.
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                if row[day] == 1:
                    service_id = row['service_id']
                    date = str(int(row['start_date']) + day_offset_to_monday)
                    date_loc = service_id + '_' + date
                    dates_dataframe.loc[date_loc] = [service_id] + [date]
                day_offset_to_monday = (day_offset_to_monday + 1) % 7

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