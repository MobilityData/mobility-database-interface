from representation.gtfs_representation import GtfsRepresentation


def process_main_language_code_for_gtfs_metadata(gtfs_representation):
    """Process the main language code using the`agency` file from the GTFS dataset of the representation.
    Add the main language code to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")

    dataset = gtfs_representation.get_dataset()

    # Extract the main language code from the first row in the dataset agency
    main_language_code = dataset.agency['agency_lang'].iloc[0]

    gtfs_representation.set_metadata_main_language_code(main_language_code)
    return gtfs_representation
