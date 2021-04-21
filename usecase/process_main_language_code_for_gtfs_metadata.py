from utilities.validators import validate_gtfs_representation
from utilities.notices import MAIN_LANGUAGE_FOR_GTFS_METADATA_NOTICES

AGENCY_LANG_KEY = "agency_lang"
AGENCY_LANG_IDX = 0
MAIN_LANGUAGE_NOTICES = MAIN_LANGUAGE_FOR_GTFS_METADATA_NOTICES


def process_main_language_code_for_gtfs_metadata(gtfs_representation):
    """Process the main language code using the`agency` file from the GTFS dataset of the representation.
    Add the main language code to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract the main language code from the first row in the dataset agency
    main_language_code = dataset.agency[AGENCY_LANG_KEY].iloc[AGENCY_LANG_IDX]

    # Set the main language code in the GTFS representation
    metadata.main_language_code = main_language_code

    return gtfs_representation
