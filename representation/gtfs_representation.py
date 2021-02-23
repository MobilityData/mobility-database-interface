from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata


class GtfsRepresentation:
    def __init__(self, entity_code, dataset, metadata):
        """Constructor for ``GtfsRepresentation``.
        :param entity_code: The entity code associated to the GTFS dataset in the database.
        :param dataset: The representation of the GTFS dataset content.
        :param metadata: The representation of the GTFS dataset metadata.
        """
        if not isinstance(entity_code, str) or not entity_code:
            raise TypeError("Entity code must be a valid non-empty entity code string.")
        self.entity_code = entity_code
        if not isinstance(dataset, Feed):
            raise TypeError("Dataset must be a valid GTFS Kit Feed.")
        self.dataset = dataset
        if not isinstance(metadata, GtfsMetadata):
            raise TypeError("Metadata must be a valid GtfsMetadata.")
        self.metadata = metadata

    def print_representation(self):
        """Print the representation of the GTFS dataset."""
        print("--------------- Metadata ---------------\n")
        print(str(self.metadata))
        print("\n--------------- Dataset ---------------\n")
        print(self.dataset)
