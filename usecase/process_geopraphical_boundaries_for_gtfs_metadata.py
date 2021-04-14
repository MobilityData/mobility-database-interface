from utilities.geographical_utils import (
    process_bounding_box_corner_floats,
    process_bounding_octagon_corner_floats,
)
from utilities.validators import validate_gtfs_representation
from utilities.notices import (
    STANDALONE,
    WITH_FILENAME,
    FILENAME,
    STOPS_TXT,
    DUPLICATED_COLUMN,
    DUPLICATE_KEY,
    EMPTY_FILE,
    INVALID_FLOAT,
    INVALID_ROW_LENGTH,
    LEADING_OR_TRAILING_WHITESPACES,
    MISSING_REQUIRED_COLUMN,
    MISSING_REQUIRED_FIELD,
    MISSING_REQUIRED_FILE,
    NEW_LINE_IN_VALUE,
    NUMBER_OUT_OF_RANGE,
    IO_ERROR,
    THREAD_EXECUTION_ERROR,
    THREAD_INTERRUPTED_ERROR,
    URI_SYNTAX_ERROR,
    RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
)

GEO_BOUNDARIES_UTILS = "geo_boundaries_utils"
GEO_BOUNDARIES_ATTR = "geo_boundaries_attr"

BOUNDING_BOX_MAP = {
    GEO_BOUNDARIES_UTILS: process_bounding_box_corner_floats,
    GEO_BOUNDARIES_ATTR: "bounding_box",
}

BOUNDING_OCTAGON_MAP = {
    GEO_BOUNDARIES_UTILS: process_bounding_octagon_corner_floats,
    GEO_BOUNDARIES_ATTR: "bounding_octagon",
}

GEO_BOUNDARIES_NOTICES = {
    STANDALONE: {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_FLOAT,
        INVALID_ROW_LENGTH,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {STOPS_TXT},
}


def process_bounding_box_for_gtfs_metadata(gtfs_representation):
    return process_geographical_boundaries_for_gtfs_metadata(
        gtfs_representation, BOUNDING_BOX_MAP
    )


def process_bounding_octagon_for_gtfs_metadata(gtfs_representation):
    return process_geographical_boundaries_for_gtfs_metadata(
        gtfs_representation, BOUNDING_OCTAGON_MAP
    )


def process_geographical_boundaries_for_gtfs_metadata(
    gtfs_representation, geo_boundaries_map
):
    """Process the geographical boundaries, according to the `geo_boundaries_map`,
    using the `stops` file from the GTFS dataset of the representation.
    Add the geographical boundaries to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param geo_boundaries_map: Either BOUNDING_BOX_MAP or BOUNDING_OCTAGON_MAP.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract the box corners coordinates in the dataset representation and
    # Order the corners inside a bounding box
    # The order is clockwise, from the South East to the North East corner
    # or
    # Extract the octagon corners coordinates in the dataset representation and
    # Order the corners inside a bounding octagon
    # The order is clockwise, from the right bottom to the right top corner
    # Documentation about dictionary comprehension can be found at:
    # https://docs.python.org/3/tutorial/datastructures.html
    geo_boundaries = {
        f"{index+1}": corner
        for index, corner in enumerate(
            geo_boundaries_map[GEO_BOUNDARIES_UTILS](dataset)
        )
    }

    # Set the bounding box in the GTFS representation
    # or
    # Set the bounding octagon in the GTFS representation
    setattr(metadata, geo_boundaries_map[GEO_BOUNDARIES_ATTR], geo_boundaries)

    return gtfs_representation
