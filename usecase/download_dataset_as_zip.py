import os
import requests
from requests import HTTPError


def download_dataset_as_zip(path_to_data, urls):
    """Download datasets as zip for the given urls.
    :param path_to_data: The path to the folder where to store the dataset zip files.
    :param urls: URLs of the dataset zip files to download.
    :return: The paths to the downloaded dataset zip files.
    """
    if not os.path.isdir(path_to_data):
        raise TypeError("Data path must be a valid path.")
    if not isinstance(urls, dict):
        raise TypeError("URLs must be a valid dictionary.")

    paths_to_datasets = {}
    for entity_code, url in urls.items():
        print(f"--------------- Downloading URL : {url} ---------------\n")
        slash_index = url.rfind("/")
        zip_name = url[slash_index + 1 :]
        zip_path = os.path.join(path_to_data, f"{entity_code}_{zip_name}")
        try:
            zip_file_req = requests.get(url, allow_redirects=True)
            zip_file_req.raise_for_status()
        except HTTPError as http_error:
            print(f'Exception "{http_error}" occurred when downloading URL\n')
            continue

        zip_file = zip_file_req.content
        with open(zip_path, "wb") as file:
            file.write(zip_file)

        paths_to_datasets[entity_code] = zip_path
        print(f"Success : {entity_code}_{zip_name} downloaded in {path_to_data}\n")
    return paths_to_datasets
