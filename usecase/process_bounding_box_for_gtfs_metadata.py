from utilities.geographical_utils import (
    process_bounding_box_corner_strings,
    process_bounding_box_corner_floats,
)
from utilities.validators import validate_gtfs_representation

BOUNDING_BOX_ATTR = "bounding_box"


def process_bounding_box_for_gtfs_metadata(gtfs_representation):
    """Execute the ``ProcessBoundingBoxForGtfsMetadata`` use case.
    Process the bounding box using the`stops` file from the GTFS dataset of the representation.
    Add the bounding box to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Extract the box corners coordinates in the dataset representation and
    # Order the corners inside a bounding box
    # The order is clockwise, from the South East to the North East corner
    # Documentation about dictionary comprehension can be found at:
    # https://docs.python.org/3/tutorial/datastructures.html
    bounding_box = {
        f"{index + 1}": corner
        for index, corner in enumerate(process_bounding_box_corner_floats(dataset))
    }

    # Set the bounding box in the GTFS representation
    setattr(metadata, BOUNDING_BOX_ATTR, bounding_box)

    return gtfs_representation
