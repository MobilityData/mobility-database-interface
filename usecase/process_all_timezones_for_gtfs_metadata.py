from representation.gtfs_representation import GtfsRepresentation

STOP_TIMEZONE_KEY = "stop_timezone"
AGENCY_TIMEZONE_KEY = "agency_timezone"


def process_all_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    dataset = gtfs_representation.get_dataset()

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
        all_timezones.add(dataset.agency[AGENCY_TIMEZONE_KEY].iloc[0])

    # Convert the set of time to a list, and sort it alphabetically
    all_timezones = sorted(list(all_timezones))

    # Set all timezones in the GTFS representation
    gtfs_representation.set_metadata_all_timezones(all_timezones)

    return gtfs_representation
