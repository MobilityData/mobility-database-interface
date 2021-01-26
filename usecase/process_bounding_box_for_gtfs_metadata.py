from representation.gtfs_representation import GtfsRepresentation
from utilities.geographical_utils import *

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

    # Extract the box corners coordinates in the dataset representation and
    # Order the corners inside a bounding box
    # The order is clockwise, from the South East to the North East corner
    bounding_box = {
        f"{index+1}": corner for index, corner in enumerate(process_bounding_box_corner_strings(dataset))
    }

    # Set the bounding box in the GTFS representation
    getattr(gtfs_representation, BOUNDING_BOX_SETTER)(bounding_box)

    return gtfs_representation
