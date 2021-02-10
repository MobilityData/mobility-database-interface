from utilities.validators import validate_gtfs_representation


def process_main_timezone_for_gtfs_metadata(gtfs_representation):
    """Process the main timezone using the`agency` file from the GTFS dataset of the representation.
    Add the main timezone to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.get_dataset()

    # Extract the main timezone from the first row in the dataset agency
    main_timezone = dataset.agency["agency_timezone"].iloc[0]

    # Set the main timezone in the GTFS representation
    gtfs_representation.set_metadata_main_timezone(main_timezone)

    return gtfs_representation
