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
BOUNDING_OCTAGON_SETTER = "set_metadata_bounding_box"


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

    # Extract the octagon corners coordinates in the dataset representation and
    # Order the corners inside a bounding octagon
    # The order is clockwise, from the right bottom to the right top corner
    bounding_octagon = {
        f"{index+1}": corner for index, corner in enumerate(process_bounding_octagon_corner_strings(dataset))
    }

    # Set the bounding octagon in the GTFS representation
    getattr(gtfs_representation, BOUNDING_OCTAGON_SETTER)(bounding_octagon)

    return gtfs_representation








