from datetime import date
import os
from pathlib import Path

import requests
from requests import HTTPError
from requests.exceptions import SSLError
from utilities.validators import validate_datasets_infos


def download_datasets_as_zip(path_to_data, datasets_infos):
    """Download datasets as zip for the given urls.
    :param path_to_data: The path to the folder where to store the dataset zip files.
    :param datasets_infos: The datasets infos from which to take the urls.
    :return: A list of DatasetInfos for which the datasets zip file have been downloaded.
    """
    if not os.path.isdir(path_to_data):
        raise TypeError("Data path must be a valid path.")
    validate_datasets_infos(datasets_infos)
    updated_datasets_infos = []

    for dataset_infos in datasets_infos:
        dataset_infos = download_dataset_as_zip(path_to_data, dataset_infos)
        updated_datasets_infos.append(dataset_infos)

    return updated_datasets_infos


def download_dataset_as_zip(path_to_data, dataset_infos):
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
        return
    except SSLError as ssl_error:
        print(f'Exception "{ssl_error}" occurred when downloading URL\n')
        return
    zip_file = zip_file_req.content

    Path(path_to_data).mkdir(parents=True, exist_ok=True)
    with open(zip_path, "wb") as file:
        file.write(zip_file)

    dataset_infos.zip_path = zip_path
    dataset_infos.download_date = date.today().strftime("%Y-%m-%d")
    print(f"Success : {entity_code}_{zip_name} downloaded in {path_to_data}\n")
    return dataset_infos
