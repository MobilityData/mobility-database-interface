from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata


class GtfsRepresentation:
    def __init__(self, entity_code, dataset, metadata):
        """Constructor for ``GtfsRepresentation``.
        :param entity_code: The entity code associated to the GTFS dataset in the database.
        :param dataset: The representation of the GTFS dataset content.
        :param metadata: The representation of the GTFS dataset metadata.
        """
        if entity_code is None or not isinstance(entity_code, str):
            raise TypeError('Entity code must be a valid entity code string.')
        self.__entity_code = entity_code
        if dataset is None or not isinstance(dataset, Feed):
            raise TypeError('Dataset must be a valid GTFS Kit Feed.')
        self.__dataset = dataset
        if metadata is None or not isinstance(metadata, GtfsMetadata):
            raise TypeError('Metadata must be a valid GtfsMetadata.')
        self.__metadata = metadata

    def print_representation(self):
        """ Print the representation of the GTFS dataset.
        """
        print("--------------- Metadata ---------------\n")
        print(str(self.__metadata))
        print("\n--------------- Dataset ---------------\n")
        print(self.__dataset)
