from datetime import date, datetime
import os
import re
import requests
from requests import HTTPError
from requests.exceptions import SSLError
from utilities.validators import validate_datasets_infos

OMD_URL_DOWNLOAD_DATE_REGEX = r"(?<=/)\w+(?=/download)"
OMD_URL_DOWNLOAD_DATE_FORMAT = "%Y%m%d"
METADATA_DOWNLOAD_DATE_FORMAT = "%Y-%m-%d"


def add_download_date_for_omd_harvesting(dataset_infos):
    date_string = re.search(OMD_URL_DOWNLOAD_DATE_REGEX, dataset_infos.url)
    date_string = date_string.group(0)
    date_string = (
        datetime.strptime(date_string, OMD_URL_DOWNLOAD_DATE_FORMAT)
        .date()
        .strftime(METADATA_DOWNLOAD_DATE_FORMAT)
    )
    dataset_infos.download_date = date_string
    return dataset_infos


def add_download_date_for_cron_job(dataset_infos):
    dataset_infos.download_date = date.today().strftime(METADATA_DOWNLOAD_DATE_FORMAT)
    return dataset_infos


def download_dataset_as_zip_for_omd_harvesting(path_to_data, datasets_infos):
    return download_dataset_as_zip(
        path_to_data, datasets_infos, add_download_date_for_omd_harvesting
    )


def download_dataset_as_zip_for_cron_job(path_to_data, datasets_infos):
    return download_dataset_as_zip(
        path_to_data, datasets_infos, add_download_date_for_cron_job
    )


def download_dataset_as_zip(path_to_data, datasets_infos, download_date_func):
    """Download datasets as zip for the given urls.
    :param path_to_data: The path to the folder where to store the dataset zip files.
    :param datasets_infos: The datasets infos from which to take the urls.
    :param download_date_func: The function to add the download date to a dataset infos.
    :return: A list of DatasetInfos for which the datasets zip file have been downloaded.
    """
    if not os.path.isdir(path_to_data):
        raise TypeError("Data path must be a valid path.")
    validate_datasets_infos(datasets_infos)
    updated_datasets_infos = []

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
        except SSLError as ssl_error:
            print(f'Exception "{ssl_error}" occurred when downloading URL\n')
            continue

        zip_file = zip_file_req.content
        with open(zip_path, "wb") as file:
            file.write(zip_file)

        dataset_infos.zip_path = zip_path
        dataset_infos = download_date_func(dataset_infos)
        print(f"Success : {entity_code}_{zip_name} downloaded in {path_to_data}\n")
        updated_datasets_infos.append(dataset_infos)

    return updated_datasets_infos
