from datetime import date
import os
import requests
from requests import HTTPError
from utilities.validators import validate_datasets_infos


def download_dataset_as_zip(path_to_data, datasets_infos):
    """Download datasets as zip for the given urls.
    :param path_to_data: The path to the folder where to store the dataset zip files.
    :param datasets_infos: The datasets infos from which to take the urls.
    :return: The datasets infos updated with the paths to the downloaded dataset zip files.
    """
    if not os.path.isdir(path_to_data):
        raise TypeError("Data path must be a valid path.")
    validate_datasets_infos(datasets_infos)

    for dataset_infos in datasets_infos:
        url = dataset_infos.url
        entity_code = dataset_infos.entity_code
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

        dataset_infos.zip_path = zip_path
        dataset_infos.download_date = date.today().strftime("%Y-%m-%d")
        print(f"Success : {entity_code}_{zip_name} downloaded in {path_to_data}\n")
    return datasets_infos
