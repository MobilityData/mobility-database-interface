import os
import requests


class DownloadDataset:
    def __init__(self, data_folder_path, urls):
        """Constructor for ``DownloadDataset``.
        :param data_folder_path: The path to the folder where to store the datasets.
        :param urls: URLs of the datasets to download.
        """
        try:
            if data_folder_path is None or not os.path.isdir(data_folder_path):
                raise TypeError("Temporary data path must be a valid path.")
            self.data_folder_path = data_folder_path
            if urls is None or not isinstance(urls, dict):
                raise TypeError("URLs must be a valid dictionary.")
            self.urls = urls
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``DownloadDataset`` use case.
        :return: The paths to the downloaded datasets.
        """
        zip_paths = {}
        for entity_code, url in self.urls.items():
            try:
                print("--------------- Downloading URL : %s ---------------\n" % url)
                zip_name = url[url.rfind("/")+1:len(url)]
                zip_path = self.data_folder_path + '%s_%s' % (entity_code, zip_name)
                zip_file = requests.get(url, allow_redirects=True)
                open(zip_path, 'wb').write(zip_file.content)
                zip_paths[entity_code] = zip_path
                print("Success : %s_%s downloaded in %s\n" % (entity_code, zip_name, self.data_folder_path))
            except Exception as e:
                print("Exception \"%s\" occurred when downloading URL\n" % e)
        return zip_paths
