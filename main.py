import argparse
from dotenv import load_dotenv
import json
from guppy import hpy
import os
from wikibaseintegrator.wbi_config import config as wbi_config
from repository.data_repository import DataRepository
from usecase.download_dataset_as_zip import download_dataset_as_zip
from usecase.process_agencies_count_for_gtfs_metadata import (
    process_agencies_count_for_gtfs_metadata,
)
from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
)
from usecase.load_dataset import load_dataset
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
)
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_box_for_gtfs_metadata,
    process_bounding_octagon_for_gtfs_metadata,
)
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
)
from usecase.process_md5 import process_md5
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
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_dataset_entity_for_gtfs_metadata,
)
from utilities.constants import (
    SPARQL_URL,
    API_URL,
    SPARQL_BIGDATA_URL,
    SVC_URL,
    USERNAME,
    PASSWORD,
)
from utilities.report_utils import clean_report
from utilities.validators import validate_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MobilityDatabase Interface Script")
    parser.add_argument(
        "--data-type",
        action="store",
        choices=["GTFS", "GBFS"],
        default="GTFS",
        help='Type of the datasets to process. Possible values : "GTFS", "GBFS".',
    )
    parser.add_argument(
        "--path-to-tmp-data",
        action="store",
        default="./data/tmp/",
        help="Path to the folder where to temporary store downloaded datasets for processing.",
    )
    parser.add_argument(
        "--path-to-env-var",
        action="store",
        default="./.env.staging",
        help="Path to the environment variables.",
    )
    parser.add_argument(
        "--path-to-credentials",
        action="store",
        default="./staging_credentials.json",
        help="Path to the credentials.",
    )
    parser.add_argument(
        "--path-to-validation-report",
        action="store",
        default="./report.json",
        help="Path to the validation report.",
    )
    parser.add_argument(
        "--path-to-system-report",
        action="store",
        default="./system_errors.json",
        help="Path to the system errors report.",
    )
    args = parser.parse_args()

    # Load and clean the reports obtained from the validation output
    with open(args.path_to_validation_report, "r") as f:
        validation_report = clean_report(json.load(f))
    with open(args.path_to_system_report, "r") as f:
        system_report = clean_report(json.load(f))

    # Load environment from dotenv file and credentials json file
    load_dotenv(args.path_to_env_var)
    with open(args.path_to_credentials) as f:
        credentials = json.load(f)
    os.environ[USERNAME] = credentials.get(USERNAME)
    os.environ[PASSWORD] = credentials.get(PASSWORD)

    # Get environment variables
    sparql_url = os.environ.get(SPARQL_URL)
    api_url = os.environ.get(API_URL)

    # Load Wikibase Integrator config with the environment
    wbi_config["MEDIAWIKI_API_URL"] = os.environ[API_URL]
    wbi_config["SPARQL_ENDPOINT_URL"] = os.environ[SPARQL_BIGDATA_URL]
    wbi_config["WIKIBASE_URL"] = SVC_URL

    # Initialize DataRepository
    data_repository = DataRepository()

    # Process data
    # Download datasets zip files
    datasets_infos = extract_gtfs_datasets_infos_from_database(
        api_url,
        sparql_url,
    )

    # Download datasets zip files
    datasets_infos = download_dataset_as_zip(args.path_to_tmp_data, datasets_infos)

    # Process the MD5 hashes
    datasets_infos = process_md5(datasets_infos)

    # Load the datasets in memory in the data repository
    data_repository = load_dataset(data_repository, datasets_infos, args.data_type)

    # Process each dataset representation in the data_repository
    for (
        dataset_key,
        dataset_representation,
    ) in data_repository.get_dataset_representations().items():
        dataset_representation = process_start_service_date_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_end_service_date_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_start_timestamp_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_end_timestamp_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_main_language_code_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_timezones_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_bounding_box_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_bounding_octagon_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_agencies_count_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_routes_count_by_type_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_stops_count_by_type_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = create_dataset_entity_for_gtfs_metadata(
            dataset_representation, api_url
        )

        # Print results
        data_repository.print_dataset_representation(dataset_key)

    # Print memory usage
    print("\n--------------- Memory Usage ---------------\n")
    print(hpy().heap())
