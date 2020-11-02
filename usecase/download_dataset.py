from repository.gtfs_data_repository import GtfsDataRepository


class DownloadDataset:
    def __init__(self, gtfs_data_repository, urls):
        """Constructor for ``DownloadDataset``.
        :param gtfs_data_repository: Data repository containing the datasets.
        :param urls: URLs of the datasets to download.
        """
        try:
            if gtfs_data_repository is None or not isinstance(gtfs_data_repository, GtfsDataRepository):
                raise TypeError("GTFS data repository must be a valid GtfsDataRepository.")
            self.gtfs_data_repository = gtfs_data_repository
            if urls is None or not isinstance(urls, dict):
                raise TypeError("URLs must be a valid dictionary.")
            self.urls = urls
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``DownloadDataset`` use case.
        :return: The data repository containing the downloaded datasets.
        """
        for key, url in self.urls.items():
            try:
                print("--------------- Downloading URL : %s ---------------\n" % url)
                self.gtfs_data_repository.add_dataset(key, url)
                self.gtfs_data_repository.display_dataset(key)
            except Exception as e:
                print("Exception \"%s\" occurred when opening URL\n" % e)

        return self.gtfs_data_repository
