from representation.gtfs_representation import GtfsRepresentation


def process_all_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    dataset = gtfs_representation.get_dataset()

    # Extract the all the timezones using the stop_timezone in the dataset stops
    all_timezones = set()
    if 'stop_timezone' in dataset.stops.columns:
        for index, row in dataset.stops.iterrows():
            if row['stop_timezone'] is not None:
                all_timezones.add(row['stop_timezone'])

    # Extract the timezone from the first row in the dataset agency
    # to add the main timezone to the set
    # if the set of all timezones is empty after processing the dataset stops
    if len(all_timezones) == 0:
        all_timezones.add(dataset.agency['agency_timezone'].iloc[0])

    # Convert the set of time to a list, and sort it alphabetically
    all_timezones = sorted(list(all_timezones))

    # Set all timezones in the GTFS representation
    gtfs_representation.set_metadata_all_timezones(all_timezones)

    return gtfs_representation
