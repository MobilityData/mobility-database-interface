from pathlib import Path
import gtfs_kit as gtfs_kit


class GtfsDataRepository:
    def __init__(self, dataset_path):
        dataset_path = Path(dataset_path)
        self.feed = gtfs_kit.read_feed(dataset_path, dist_units='km')

    def display_dataset(self):
        print(self.feed)

    def get_dataset(self):
        return self.feed
