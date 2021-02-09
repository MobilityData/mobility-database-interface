import os
import requests


class DownloadDatasetAsZip:
    def __init__(self, path_to_data, urls):
        """Constructor for ``DownloadDatasetAsZip``.
        :param path_to_data: The path to the folder where to store the dataset zip files.
        :param urls: URLs of the dataset zip files to download.
        """
        try:
            if path_to_data is None or not os.path.isdir(path_to_data):
                raise TypeError("Data path must be a valid path.")
            self.data_folder_path = path_to_data
            if urls is None or not isinstance(urls, dict):
                raise TypeError("URLs must be a valid dictionary.")
            self.urls = urls
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``DownloadDatasetAsZip`` use case.
        :return: The paths to the downloaded dataset zip files.
        """
        paths_to_datasets = {}
        for entity_code, url in self.urls.items():
            try:
                print("--------------- Downloading URL : %s ---------------\n" % url)
                zip_name = url[url.rfind("/") + 1 : len(url)]
                zip_path = self.data_folder_path + "%s_%s" % (entity_code, zip_name)
                zip_file = requests.get(url, allow_redirects=True)
                open(zip_path, "wb").write(zip_file.content)
                paths_to_datasets[entity_code] = zip_path
                print(
                    "Success : %s_%s downloaded in %s\n"
                    % (entity_code, zip_name, self.data_folder_path)
                )
            except Exception as e:
                print('Exception "%s" occurred when downloading URL\n' % e)
        return paths_to_datasets
