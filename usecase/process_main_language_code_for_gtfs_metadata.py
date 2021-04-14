from utilities.validators import validate_gtfs_representation
from utilities.notices import (
    INCONSISTENT_AGENCY_TIMEZONE,
    DUPLICATED_COLUMN,
    DUPLICATE_KEY,
    EMPTY_FILE,
    INVALID_COLOR,
    INVALID_CURRENCY,
    INVALID_DATE,
    INVALID_EMAIL,
    INVALID_FLOAT,
    INVALID_INTEGER,
    INVALID_LANGUAGE_CODE,
    INVALID_PHONE_NUMBER,
    INVALID_ROW_LENGTH,
    INVALID_TIME,
    INVALID_TIMEZONE,
    INVALID_URL,
    LEADING_OR_TRAILING_WHITESPACES,
    MISSING_REQUIRED_COLUMN,
    MISSING_REQUIRED_FIELD,
    MISSING_REQUIRED_FILE,
    NEW_LINE_IN_VALUE,
    NUMBER_OUT_OF_RANGE,
    START_AND_END_RANGE_OUT_OF_ORDER,
    START_AND_END_RANGE_EQUAL,
    SAME_NAME_AND_DESCRIPTION_FOR_ROUTE,
    IO_ERROR,
    THREAD_EXECUTION_ERROR,
    THREAD_INTERRUPTED_ERROR,
    URI_SYNTAX_ERROR,
    RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
)

AGENCY_LANG_KEY = "agency_lang"
AGENCY_LANG_IDX = 0

MAIN_LANGUAGE_NOTICES = {
    "validation_errors_standalone": {INCONSISTENT_AGENCY_TIMEZONE},
    "validation_errors_with_filename": {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
    },
    "system_errors_standalone": {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
    },
    "system_errors_with_filename": {RUNTIME_EXCEPTION_IN_LOADER_ERROR},
    "system_errors_with_classname": {RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR},
    "filename": {"agency.txt"},
}


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
