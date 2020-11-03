

class DataRepository:
    def __init__(self):
        """Constructor for ``DataRepository``.
        """
        self.__dataset_representations = {}

    def add_dataset_representation(self, dataset_key, dataset_representation):
        """Add a dataset representation to the repository.
        :param dataset_key: Key to access the dataset representation in the repository.
        :param dataset_representation: The dataset representation to add to the repository.
        """
        self.__dataset_representations[dataset_key] = dataset_representation

    def display_datasets(self):
        """Print the dataset representations in the repository.
        """
        for key, representation in self.__dataset_representations.items():
            print("--------------- Dataset representation for entity %s ---------------\n" % key)
            print(representation.print_representation())

    def display_dataset(self, dataset_key):
        """Print the dataset representation accessible with the given key.
        :param dataset_key: Key to access the dataset representation in the repository.
        """
        if dataset_key in self.__dataset_representations:
            print(self.__dataset_representations[dataset_key].print_representation())

    def get_dataset_representations(self):
        """
        :return: the dataset representations in the repository.
        """
        return self.__dataset_representations

    def get_dataset_representation(self, dataset_key):
        """
        :param dataset_key: Key to access the dataset representation in the repository.
        :return: The dataset representation accessible with the given key if the `dataset_key` exists in repository,
        None otherwise.
        """
        if dataset_key in self.__dataset_representations:
            return self.__dataset_representations[dataset_key]
