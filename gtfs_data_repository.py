from pathlib import Path
import gtfs_kit as gk


class GtfsDataRepository:
    def __init__(self, feed_path):
        data_dir = '../data/'
        feed_path = Path(data_dir + feed_path)
        self.feed = gk.read_feed(feed_path, dist_units='km')

    def display_feed(self):
        print(self.feed)
