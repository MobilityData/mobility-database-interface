

class GtfsRepresentation:
    def __init__(self, entity_code, dataset, metadata):
        """Constructor for ``GtfsRepresentation``.
        :param entity_code: The entity code associated to the GTFS dataset in the database.
        :param dataset: The representation of the GTFS dataset content.
        :param metadata: The representation of the GTFS dataset metadata.
        """
        self.__entity_code = entity_code
        self.__dataset = dataset
        self.__metadata = metadata

    def print_representation(self):
        """ Print the representation of the GTFS dataset.
        """
        print("--------------- Metadata ---------------\n")
        print(str(self.__metadata))
        print("\n--------------- Dataset ---------------\n")
        print(self.__dataset)
