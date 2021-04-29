import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from guppy import hpy
from wikibaseintegrator.wbi_config import config as wbi_config

from helpers_cf import (
    decode_message,
    add_source_and_dispatch,
    add_dataset_to_source,
)
from repository.data_repository import DataRepository
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_dataset_entity_for_gtfs_metadata,
)
from usecase.download_dataset_as_zip import (
    download_datasets_as_zip,
)
from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
)
from usecase.load_dataset import load_datasets, GBFS_TYPE, GTFS_TYPE
from usecase.process_agencies_count_for_gtfs_metadata import (
    process_agencies_count_for_gtfs_metadata,
)
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_box_for_gtfs_metadata,
    process_bounding_octagon_for_gtfs_metadata,
)
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
)
from usecase.process_md5 import process_datasets_md5
from usecase.process_routes_count_by_type_for_gtfs_metadata import (
    process_routes_count_by_type_for_gtfs_metadata,
)
from usecase.process_service_date_for_gtfs_metadata import (
    process_start_service_date_for_gtfs_metadata,
    process_end_service_date_for_gtfs_metadata,
)
from usecase.process_stops_count_by_type_for_gtfs_metadata import (
    process_stops_count_by_type_for_gtfs_metadata,
)
from usecase.process_timestamp_for_gtfs_metadata import (
    process_start_timestamp_for_gtfs_metadata,
    process_end_timestamp_for_gtfs_metadata,
)
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
)
from utilities.constants import (
    SPARQL_URL,
    API_URL,
    SPARQL_BIGDATA_URL,
    SVC_URL,
    USERNAME,
    PASSWORD,
    SOURCE_NAME,
    STABLE_URL,
    VERSIONS,
    DATASET_URL,
    SOURCE_ENTITY_ID,
    DATATYPE,
)

BASE_DIR = Path(__file__).resolve().parent
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="MobilityDatabase Interface Script")
#     parser.add_argument(
#         "--data-type",
#         action="store",
#         choices=["GTFS", "GBFS"],
#         default="GTFS",
#         help='Type of the datasets to process. Possible values : "GTFS", "GBFS".',
#     )
#     parser.add_argument(
#         "--path-to-tmp-data",
#         action="store",
#         default="./data/tmp/",
#         help="Path to the folder where to temporary store downloaded datasets for processing.",
#     )
#     parser.add_argument(
#         "--path-to-env-var",
#         action="store",
#         default="./.env.staging",
#         help="Path to the environment variables.",
#     )
#     parser.add_argument(
#         "--path-to-credentials",
#         action="store",
#         default="./staging_credentials.json",
#         help="Path to the credentials.",
#     )
#     args = parser.parse_args()
#
#     # Load environment from dotenv file and credentials json file
#     load_dotenv(args.path_to_env_var)
#     with open(args.path_to_credentials) as f:
#         credentials = json.load(f)
#     os.environ[USERNAME] = credentials.get(USERNAME)
#     os.environ[PASSWORD] = credentials.get(PASSWORD)
#
#     # Get environment variables
#     sparql_url = os.environ.get(SPARQL_URL)
#     api_url = os.environ.get(API_URL)
#
#     # Load Wikibase Integrator config with the environment
#     wbi_config["MEDIAWIKI_API_URL"] = os.environ[API_URL]
#     wbi_config["SPARQL_ENDPOINT_URL"] = os.environ[SPARQL_BIGDATA_URL]
#     wbi_config["WIKIBASE_URL"] = SVC_URL
#
#     # Initialize DataRepository
#     data_repository = DataRepository()
#
#     # Process data
#     # Download datasets zip files
#     datasets_infos = extract_gtfs_datasets_infos_from_database(
#         api_url,
#         sparql_url,
#     )
#
#     # Download datasets zip files
#     datasets_infos = download_datasets_as_zip(args.path_to_tmp_data, datasets_infos)
#
#     # Process the MD5 hashes
#     datasets_infos = process_datasets_md5(datasets_infos)
#
#     # Load the datasets in memory in the data repository
#     data_repository = load_datasets(data_repository, datasets_infos, args.data_type)
#
#     # Process each dataset representation in the data_repository
#     for (
#         dataset_key,
#         dataset_representation,
#     ) in data_repository.get_dataset_representations().items():
#         dataset_representation = process_start_service_date_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_end_service_date_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_start_timestamp_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_end_timestamp_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_main_language_code_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_timezones_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_bounding_box_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_bounding_octagon_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_agencies_count_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_routes_count_by_type_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = process_stops_count_by_type_for_gtfs_metadata(
#             dataset_representation
#         )
#         dataset_representation = create_dataset_entity_for_gtfs_metadata(
#             dataset_representation, api_url
#         )
#
#         # Print results
#         data_repository.print_dataset_representation(dataset_key)
#
#     # Print memory usage
#     print("\n--------------- Memory Usage ---------------\n")
#     print(hpy().heap())
#


def add_new_source_cf(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    This Cloud Function adds a new source in the database
    and publishes several messages (as many as there are dataset versions + stable url version)
    in the before-dispatcher topic.

     It takes a message of the following structure:
     {
         "soure_name": "somestr",
         "stable_url": "someurl",
         "versions": [ "someurl", "someurl", ... ],
         "datatype": "somestr"
    }

     Args:
          event (dict):
             The dictionary with data specific to this type of
          event.
             The `data` field contains the PubsubMessage message.
             The `attributes` field will contain custom attributes if there are any.
          context (google.cloud.functions.Context):
             The Cloud Functions event metadata.
             The `event_id` field contains the Pub/Sub message ID.
             The `timestamp` field contains the publish time.
    """
    if os.getenv("ENV") == "prod":
        load_dotenv(f"{BASE_DIR}/.env.production")
    else:
        load_dotenv(f"{BASE_DIR}/.env.staging")

    message = decode_message(event)
    source_name = message[SOURCE_NAME]
    stable_url = message[STABLE_URL]
    versions = message[VERSIONS]
    datatype = message[DATATYPE]
    source_entity_id = add_source_and_dispatch(
        source_name, stable_url, versions, datatype
    )
    return source_entity_id


def add_dataset_to_source_cf(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    This Cloud Function adds a new source in the database
    and publishes several messages (as many as there are dataset versions + stable url version)
    in the before-dispatcher topic.

     It takes a message of the following structure:
     {
         "soure_name": "somestr",
         "dataset_url": "someurl",
         "source_entity_id": "someentityid"
         "datatype": "somedatatype" # must be GTFS or GBFS
    }

     Args:
          event (dict):
             The dictionary with data specific to this type of
          event.
             The `data` field contains the PubsubMessage message.
             The `attributes` field will contain custom attributes if there are any.
          context (google.cloud.functions.Context):
             The Cloud Functions event metadata.
             The `event_id` field contains the Pub/Sub message ID.
             The `timestamp` field contains the publish time.
    """
    if os.getenv("ENV") == "prod":
        load_dotenv(f"{BASE_DIR}/.env.production")
    else:
        load_dotenv(f"{BASE_DIR}/.env.staging")

    message = decode_message(event)

    source_name = message[SOURCE_NAME]
    dataset_url = message[DATASET_URL]
    source_entity_id = message[SOURCE_ENTITY_ID]
    dataset_data_type = message[DATATYPE]
    if dataset_data_type not in [GTFS_TYPE, GBFS_TYPE]:
        raise Exception(f"{dataset_data_type} is invalid")
    add_dataset_to_source(source_name, dataset_url, source_entity_id, dataset_data_type)
