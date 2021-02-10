from utilities.geographical_utils import process_bounding_octagon_corner_strings
from utilities.validators import validate_gtfs_representation

BOUNDING_OCTAGON_SETTER = "set_metadata_bounding_octagon"


def process_bounding_octagon_for_gtfs_metadata(gtfs_representation):
    """Execute the ``ProcessBoundingOctagonForGtfsMetadata`` use case.
    Process the bounding octagon using the`stops` file from the GTFS dataset of the representation.
    Add the bounding octagon to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.get_dataset()

    # Extract the octagon corners coordinates in the dataset representation and
    # Order the corners inside a bounding octagon
    # The order is clockwise, from the right bottom to the right top corner
    # Documentation about dictionary comprehension can be found at:
    # https://docs.python.org/3/tutorial/datastructures.html
    bounding_octagon = {
        f"{index+1}": corner
        for index, corner in enumerate(process_bounding_octagon_corner_strings(dataset))
    }

    # Set the bounding octagon in the GTFS representation
    getattr(gtfs_representation, BOUNDING_OCTAGON_SETTER)(bounding_octagon)

    return gtfs_representation
