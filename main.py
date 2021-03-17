from dotenv import load_dotenv
import argparse
import sys
from guppy import hpy


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
    parser.add_argument(
        "--path_to_env_var",
        action="store",
        default="./data/tmp/",
        help="Path to the folder where to temporary store downloaded datasets for processing.",
    )
    args = parser.parse_args()

    # Load environment
    load_dotenv(args.path_to_env_var)

    # Import project files
    from repository.data_repository import DataRepository
    from usecase.download_dataset_as_zip import download_dataset_as_zip
    from usecase.process_agencies_count_for_gtfs_metadata import (
        process_agencies_count_for_gtfs_metadata,
    )
    from usecase.extract_datasets_infos_from_database import (
        extract_gtfs_datasets_infos_from_database,
        extract_gbfs_datasets_infos_from_database,
    )
    from usecase.load_dataset import load_dataset
    from usecase.process_all_timezones_for_gtfs_metadata import (
        process_all_timezones_for_gtfs_metadata,
    )
    from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
        process_bounding_box_for_gtfs_metadata,
        process_bounding_octagon_for_gtfs_metadata,
    )
    from usecase.process_main_language_code_for_gtfs_metadata import (
        process_main_language_code_for_gtfs_metadata,
    )
    from usecase.process_main_timezone_for_gtfs_metadata import (
        process_main_timezone_for_gtfs_metadata,
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
    from utilities.constants import SPARQL_URL, API_URL

    # Initialize DataRepository
    data_repository = DataRepository()

    # Process data
    if args.download is not None:
        # Download datasets zip files
        datasets_infos = extract_gtfs_datasets_infos_from_database(
            API_URL,
            SPARQL_URL,
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
            dataset_representation = process_main_timezone_for_gtfs_metadata(
                dataset_representation
            )
            dataset_representation = process_all_timezones_for_gtfs_metadata(
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
                dataset_representation, API_URL
            )

            # Print results
            data_repository.print_dataset_representation(dataset_key)

    elif args.load is not None:
        # Load dataset in memory
        # TODO dataset = load_data(args['load'])
        pass

    # Print memory usage
    print("\n--------------- Memory Usage ---------------\n")
    print(hpy().heap())
