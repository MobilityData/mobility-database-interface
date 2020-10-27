

class DownloadDataset:
    def __init__(self, gtfs_data_repository, urls):
        self.gtfs_data_repository = gtfs_data_repository
        self.urls = urls

    def execute(self):
        for key, url in self.urls.items():
            try:
                print("--------------- URL : %s ---------------\n" % url)
                self.gtfs_data_repository.add_dataset(key, url)
                self.gtfs_data_repository.display_dataset(key)
            except Exception as e:
                print("Exception \"%s\" occurred when opening URL\n" % e)
