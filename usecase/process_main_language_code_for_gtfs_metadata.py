from utilities.validators import validate_gtfs_representation


def process_main_language_code_for_gtfs_metadata(gtfs_representation):
    """Process the main language code using the`agency` file from the GTFS dataset of the representation.
    Add the main language code to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.get_dataset()

    # Extract the main language code from the first row in the dataset agency
    main_language_code = dataset.agency["agency_lang"].iloc[0]

    # Set the main language code in the GTFS representation
    gtfs_representation.set_metadata_main_language_code(main_language_code)

    return gtfs_representation
