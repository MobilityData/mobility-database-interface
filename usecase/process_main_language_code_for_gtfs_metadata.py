from utilities.validators import validate_gtfs_representation
from utilities.constants import AGENCY_LANG

AGENCY_LANG_IDX = 0


def process_main_language_code_for_gtfs_metadata(gtfs_representation):
    """Process the main language code using the`agency` file from the GTFS dataset of the representation.
    Add the main language code to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Agency must be present AND not empty because we are accessing the first index
    agency_is_present = (
        dataset.agency is not None
        and AGENCY_LANG in dataset.agency.columns
        and not dataset.agency.empty
    )

    if agency_is_present:
        # Extract the main language code from the first row in the dataset agency
        main_language_code = dataset.agency[AGENCY_LANG].iloc[AGENCY_LANG_IDX]

        # Set the main language code in the GTFS representation
        # if not an empty string
        if len(main_language_code) != 0:
            metadata.main_language_code = main_language_code

    return gtfs_representation
