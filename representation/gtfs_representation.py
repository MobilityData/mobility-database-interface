

class GtfsRepresentation:
    def __init__(self, entity_code, dataset, metadata):
        self.__entity_code = entity_code
        self.__dataset = dataset
        self.__metadata = metadata

    def print_representation(self):
        print("--------------- Metadata ---------------\n")
        print(self.__metadata.print())
        print("\n--------------- Dataset ---------------\n")
        print(self.__dataset)
