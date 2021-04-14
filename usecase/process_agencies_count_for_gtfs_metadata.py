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


AGENCY_NAME_KEY = "agency_name"

AGENCIES_COUNT_NOTICES = {
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
