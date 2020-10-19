from pathlib import Path
import gtfs_kit as gtfs_kit


class GtfsDataRepository:
    def __init__(self, dataset_path):
        """Constructor for ``GtfsDataRepository``.
        :param dataset_path: Path to the dataset to load in memory.
        """
        dataset_path = Path(dataset_path)
        self.dataset = gtfs_kit.read_feed(dataset_path, dist_units='km')

    def display_dataset(self):
        """Print the dataset loaded in memory.
        """
        print(self.dataset)

    def get_dataset(self):
        """
        :return: The dataset loaded in memory.
        """
        return self.dataset
