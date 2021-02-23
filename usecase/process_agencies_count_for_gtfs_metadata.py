from utilities.validators import validate_gtfs_representation

AGENCY_NAME_KEY = "agency_name"


def process_agencies_count_for_gtfs_metadata(gtfs_representation):
    """Process and count all the agencies in the `agency` file from the GTFS dataset of the representation.
    Add the agencies count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Count agencies
    agencies_count = dataset.agency[AGENCY_NAME_KEY].size

    # Set the main timezone in the GTFS representation
    metadata.agencies_count = agencies_count

    return gtfs_representation
