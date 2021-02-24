from utilities.validators import validate_gtfs_representation

STOP_TIMEZONE_KEY = "stop_timezone"
AGENCY_TIMEZONE_KEY = "agency_timezone"
AGENCY_TIMEZONE_IDX = 0


def process_all_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract the all the timezones using the stop_timezone in the dataset stops
    all_timezones = set()
    if STOP_TIMEZONE_KEY in dataset.stops.columns:
        for index, row in dataset.stops.iterrows():
            if row[STOP_TIMEZONE_KEY] is not None:
                all_timezones.add(row[STOP_TIMEZONE_KEY])

    # Extract the timezone from the first row in the dataset agency
    # to add the main timezone to the set
    # if the set of all timezones is empty after processing the dataset stops
    if len(all_timezones) == 0:
        all_timezones.add(dataset.agency[AGENCY_TIMEZONE_KEY].iloc[AGENCY_TIMEZONE_IDX])

    # Convert the set of time to a list, and sort it alphabetically
    all_timezones = sorted(list(all_timezones))

    # Set all timezones in the GTFS representation
    metadata.all_timezones = all_timezones

    return gtfs_representation
