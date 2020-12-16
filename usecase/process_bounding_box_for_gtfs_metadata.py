from representation.gtfs_representation import GtfsRepresentation
from utilities.geographical_utils import *


class ProcessBoundingBoxForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessBoundingBoxForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessBoundingBoxForGtfsMetadata`` use case. Process the bounding box using the`stops` file
        from the GTFS dataset of the representation. Add the bounding box to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the geographical coordinates in the dataset representation
        max_lat, min_lat, max_lon, min_lon = get_geographical_coordinates(dataset)

        # Create the corner strings
        south_east_corner = min_lat + ", " + max_lon
        south_west_corner = min_lat + ", " + min_lon
        north_west_corner = max_lat + ", " + min_lon
        north_east_corner = max_lat + ", " + max_lon

        # Order the corners inside a bounding box
        bounding_box = {"1": south_east_corner,
                        "2": south_west_corner,
                        "3": north_west_corner,
                        "4": north_east_corner}

        self.gtfs_representation.set_metadata_bounding_box(bounding_box)
        return self.gtfs_representation
