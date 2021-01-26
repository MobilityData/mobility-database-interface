from representation.gtfs_representation import GtfsRepresentation
from utilities.geographical_utils import *

SOUTH_EAST_CORNER_KEY = "1"
SOUTH_WEST_CORNER_KEY = "2"
NORTH_WEST_CORNER_KEY = "3"
NORTH_EAST_CORNER_KEY = "4"
BOUNDING_BOX_SETTER = "set_metadata_bounding_box"


def process_bounding_box_for_gtfs_metadata(gtfs_representation):
    """Execute the ``ProcessBoundingBoxForGtfsMetadata`` use case.
    Process the bounding box using the`stops` file from the GTFS dataset of the representation.
    Add the bounding box to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    dataset = gtfs_representation.get_dataset()

    # Extract the box corners coordinates in the dataset representation
    (
        south_east_corner,
        south_west_corner,
        north_west_corner,
        north_east_corner,
    ) = process_bounding_box_corner_strings(dataset)

    # Order the corners inside a bounding box
    bounding_box = {
        SOUTH_EAST_CORNER_KEY: south_east_corner,
        SOUTH_WEST_CORNER_KEY: south_west_corner,
        NORTH_WEST_CORNER_KEY: north_west_corner,
        NORTH_EAST_CORNER_KEY: north_east_corner,
    }

    # Set the bounding box in the GTFS representation
    getattr(gtfs_representation, BOUNDING_BOX_SETTER)(bounding_box)

    return gtfs_representation
