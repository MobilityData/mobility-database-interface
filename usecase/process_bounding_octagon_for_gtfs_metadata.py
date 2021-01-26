from representation.gtfs_representation import GtfsRepresentation
from utilities.geographical_utils import *

RIGHT_BOTTOM_CORNER_KEY = "1"
BOTTOM_RIGHT_CORNER_KEY = "2"
BOTTOM_LEFT_CORNER_KEY = "3"
LEFT_BOTTOM_CORNER_KEY = "4"
LEFT_TOP_CORNER_KEY = "5"
TOP_LEFT_CORNER_KEY = "6"
TOP_RIGHT_CORNER_KEY = "7"
RIGHT_TOP_CORNER_KEY = "8"
BOUNDING_BOX_SETTER = "set_metadata_bounding_box"


def process_bounding_octagon_for_gtfs_metadata(gtfs_representation):
    """Execute the ``ProcessBoundingOctagonForGtfsMetadata`` use case.
    Process the bounding octagon using the`stops` file from the GTFS dataset of the representation.
    Add the bounding octagon to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    dataset = gtfs_representation.get_dataset()

    # Extract the octagon corners coordinates in the dataset representation
    (
        right_bottom_corner,
        bottom_right_corner,
        bottom_left_corner,
        left_bottom_corner,
        left_top_corner,
        top_left_corner,
        top_right_corner,
        right_top_corner
    ) = process_bounding_octagon_corner_strings(dataset)

    # Order the corners inside a bounding octagon
    bounding_octagon = {RIGHT_BOTTOM_CORNER_KEY: right_bottom_corner,
                        BOTTOM_RIGHT_CORNER_KEY: bottom_right_corner,
                        BOTTOM_LEFT_CORNER_KEY: bottom_left_corner,
                        LEFT_BOTTOM_CORNER_KEY: left_bottom_corner,
                        LEFT_TOP_CORNER_KEY: left_top_corner,
                        TOP_LEFT_CORNER_KEY: top_left_corner,
                        TOP_RIGHT_CORNER_KEY: top_right_corner,
                        RIGHT_TOP_CORNER_KEY: right_top_corner}

    gtfs_representation.set_metadata_bounding_octagon(bounding_octagon)
    return gtfs_representation








