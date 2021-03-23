import argparse
import sys
import requests
from guppy import hpy


from repository.data_repository import DataRepository
from request_manager.sparql_request_helper import sparql_request
from usecase.compare_gtfs_stops import CompareGtfsStops
from usecase.download_dataset_as_zip import download_dataset_as_zip
from usecase.process_agencies_count_for_gtfs_metadata import (
    process_agencies_count_for_gtfs_metadata,
)
from usecase.extract_datasets_infos_from_database import (
    extract_gtfs_datasets_infos_from_database,
    extract_gbfs_datasets_infos_from_database,
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
from utilities.constants import STAGING_SPARQL_URL, STAGING_API_URL


def compare_stops(dataset):
    compare_dataset_stops = CompareGtfsStops(dataset, dataset)
    compare_dataset_stops.execute()


def create_datasets_infos_dictionary(
    paths_to_datasets_and_md5, sources_name, download_date
):
    datasets_infos = {}
    for entity_code in paths_to_datasets_and_md5.keys():
        paths_to_datasets_and_md5[entity_code]["source_name"] = sources_name[
            entity_code
        ]
        paths_to_datasets_and_md5[entity_code]["download_date"] = download_date
        datasets_infos[entity_code] = paths_to_datasets_and_md5[entity_code]
    return datasets_infos


def print_items_by_query(query):
    # Get all data from Wikibase image
    # Can be also use to get all related data to an entity,
    # i.e. all sub-entities of "Public transport operator", like STM, MBTA, etc.
    sparql_response = sparql_request(STAGING_SPARQL_URL, query)
    results = []
    print(sparql_response)
    for result in sparql_response["results"]["bindings"]:
        print(result)
        print(result["a"]["value"][37:40])
        results.append(result["a"]["value"][37:40])

    # Get data for a specific entity from Wikibase image
    for result in results:
        params = {
            "action": "wbgetentities",
            "ids": "%s" % result,
            "languages": "en",
            "format": "json",
        }
        api_request = requests.get(STAGING_API_URL, params)
        print(api_request)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MobilityDatabase Interface Script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--data_type",
        action="store",
        choices=["GTFS", "GBFS"],
        default="GTFS",
        help='Type of the datasets to process. Possible values : "GTFS", "GBFS".',
    )
    group.add_argument(
        "--download",
        action="store_const",
        const=True,
        help="Download datasets in memory. Usage : --download (-a | -s SPECIFIC)",
    )
    group.add_argument(
        "--load",
        action="store",
        help="Load a dataset in memory. Must include path "
        "to the dataset zip file as positional argument.",
    )
    download_group = parser.add_mutually_exclusive_group(
        required="--download" in sys.argv
    )
    download_group.add_argument(
        "-a",
        "--all",
        action="store_const",
        const=True,
        help="Download all datasets found for a type in the Mobility Database."
        'Required with --download to select the "Download all" option.',
    )
    download_group.add_argument(
        "-s",
        "--specific",
        action="store",
        help="Download the dataset related to an entity code in the Mobility Database. "
        "Entity code for the specific dataset to download must be valid and provided "
        "as positional argument. Required with --download to select "
        'the "Download specific" option.',
    )
    parser.add_argument(
        "--path_to_tmp_data",
        action="store",
        default="./data/tmp/",
        help="Path to the folder where to temporary store downloaded datasets for processing.",
    )
    args = vars(parser.parse_args())

    # Initialize DataRepository
    data_repository = DataRepository()

    # Process data
    if args["download"] is not None:
        # Download datasets zip files
        datasets_infos = extract_gtfs_datasets_infos_from_database(
            STAGING_API_URL,
            STAGING_SPARQL_URL,
        )

        # Download datasets zip files
        datasets_infos = download_dataset_as_zip(
            args["path_to_tmp_data"], datasets_infos
        )

        # Process the MD5 hashes
        datasets_infos = process_md5(datasets_infos)

        # Load the datasets in memory in the data repository
        data_repository = load_dataset(
            data_repository, datasets_infos, args["data_type"]
        )

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
                dataset_representation, STAGING_API_URL
            )

            # Print results
            data_repository.print_dataset_representation(dataset_key)

    elif args["load"] is not None:
        # Load dataset in memory
        # TODO dataset = load_data(args['load'])
        pass

    # Print memory usage
    print("\n--------------- Memory Usage ---------------\n")
    print(hpy().heap())
