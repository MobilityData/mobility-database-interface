from representation.gtfs_representation import GtfsRepresentation
from utilities.geographical_utils import *


class ProcessBoundingOctagonForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessBoundingOctagonForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessBoundingOctagonForGtfsMetadata`` use case.
        Process the bounding octagon using the`stops` file from the GTFS dataset of the representation.
        Add the bounding octagon to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the octagon corners coordinates in the dataset representation
        octagon_corners = process_bounding_octagon_corner_strings(dataset)

        right_bottom_corner = octagon_corners[0]
        bottom_right_corner = octagon_corners[1]
        bottom_left_corner = octagon_corners[2]
        left_bottom_corner = octagon_corners[3]
        left_top_corner = octagon_corners[4]
        top_left_corner = octagon_corners[5]
        top_right_corner = octagon_corners[6]
        right_top_corner = octagon_corners[7]

        # Order the corners inside a bounding octagon
        bounding_octagon = {"1": right_bottom_corner,
                            "2": bottom_right_corner,
                            "3": bottom_left_corner,
                            "4": left_bottom_corner,
                            "5": left_top_corner,
                            "6": top_left_corner,
                            "7": top_right_corner,
                            "8": right_top_corner}

        self.gtfs_representation.set_metadata_bounding_octagon(bounding_octagon)
        return self.gtfs_representation
