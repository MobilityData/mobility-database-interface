from pathlib import Path
import gtfs_kit as gtfs_kit


class GtfsDataRepository:
    def __init__(self, feed_path):
        data_dir = '../data/'
        feed_path = Path(data_dir + feed_path)
        self.feed = gtfs_kit.read_feed(feed_path, dist_units='km')

    def display_feed(self):
        print(self.feed)

    def get_feed(self):
        return self.feed
