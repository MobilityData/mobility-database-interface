from utilities.validators import validate_gtfs_representation
from utilities.constants import AGENCY_NAME


def process_agencies_count_for_gtfs_metadata(gtfs_representation):
    """Process and count all the agencies in the `agency` file from the GTFS dataset of the representation.
    Add the agencies count to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    is_agency_present = (
        dataset.agency is not None and AGENCY_NAME in dataset.agency.columns
    )

    if is_agency_present:
        # Count agencies
        agencies_count = dataset.agency[AGENCY_NAME].size
    else:
        agencies_count = 0

    # Set the main timezone in the GTFS representation
    metadata.agencies_count = agencies_count

    return gtfs_representation
