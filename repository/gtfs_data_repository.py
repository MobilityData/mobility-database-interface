import gtfs_kit as gtfs_kit


class GtfsDataRepository:
    def __init__(self):
        """Constructor for ``GtfsDataRepository``.
        """
        self.datasets = {}

    def add_dataset(self, dataset_key, dataset_path):
        """Add a dataset to the repository.
        :param dataset_key: Key to access the dataset in the repository.
        :param dataset_path: Path to the dataset to add to the repository.
        """
        self.datasets[dataset_key] = gtfs_kit.read_feed(dataset_path, dist_units='km')

    def display_datasets(self):
        """Print the datasets in the repository.
        """
        print(self.datasets)

    def display_dataset(self, dataset_key):
        """Print the dataset accessible with the given key.
        :param dataset_key: Key to access the dataset in the repository.
        """
        if dataset_key in self.datasets:
            print(self.datasets[dataset_key])

    def get_datasets(self):
        """
        :return: the datasets in the repository.
        """
        return self.datasets

    def get_dataset(self, dataset_key):
        """
        :param dataset_key: Key to access the dataset in the repository.
        :return: The dataset accessible with the given key if the `dataset_key` exists in repository, None otherwise.
        """
        if dataset_key in self.datasets:
            return self.datasets[dataset_key]
