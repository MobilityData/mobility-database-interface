from utilities.validators import validate_gtfs_representation

STOP_TIMEZONE_KEY = "stop_timezone"
AGENCY_TIMEZONE_KEY = "agency_timezone"
AGENCY_TIMEZONE_IDX = 0


def process_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract main timezone
    main_timezone = dataset.agency[AGENCY_TIMEZONE_KEY].iloc[AGENCY_TIMEZONE_IDX]

    # Extract the all the timezones using the stop_timezone in the dataset stops
    stop_timezones = set()
    if STOP_TIMEZONE_KEY in dataset.stops.columns:
        for index, row in dataset.stops.iterrows():
            if row[STOP_TIMEZONE_KEY] is not None:
                stop_timezones.add(row[STOP_TIMEZONE_KEY])

    # Extract the timezone from the first row in the dataset agency
    # to add the main timezone to the set
    # if the set of all timezones is empty after processing the dataset stops
    other_timezones = []
    if len(stop_timezones) != 0:
        other_timezones = stop_timezones
        other_timezones.discard(main_timezone)
        # Convert the set of time to a list, and sort it alphabetically
        other_timezones = sorted(list(other_timezones))

    # Set all timezones in the GTFS representation
    metadata.main_timezone = main_timezone
    metadata.other_timezones = other_timezones

    return gtfs_representation
