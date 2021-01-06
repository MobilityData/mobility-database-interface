import argparse
import sys
from guppy import hpy
from repository.data_repository import DataRepository
from representation.dataset_representation_factory import DatasetRepresentationFactory
from request_manager.request_manager_containers import Managers
from usecase.compare_gtfs_stops import CompareGtfsStops
from usecase.download_dataset_as_zip import DownloadDatasetAsZip
from usecase.extract_sources_url import ExtractSourcesUrl
from usecase.extract_database_md5 import ExtractDatabaseMd5
from usecase.load_dataset import LoadDataset
from usecase.process_main_language_code_for_gtfs_metadata import ProcessMainLanguageCodeForGtfsMetadata
from usecase.process_main_timezone_for_gtfs_metadata import ProcessMainTimezoneForGtfsMetadata
from usecase.process_all_timezones_for_gtfs_metadata import ProcessAllTimezonesForGtfsMetadata
from usecase.process_bounding_box_for_gtfs_metadata import ProcessBoundingBoxForGtfsMetadata
from usecase.process_bounding_octagon_for_gtfs_metadata import ProcessBoundingOctagonForGtfsMetadata
from usecase.process_md5 import ProcessMd5
from usecase.process_start_service_date_for_gtfs_metadata import ProcessStartServiceDateForGtfsMetadata
from usecase.process_end_service_date_for_gtfs_metadata import ProcessEndServiceDateForGtfsMetadata
from usecase.process_start_timestamp_for_gtfs_metadata import ProcessStartTimestampForGtfsMetadata
from usecase.process_end_timestamp_for_gtfs_metadata import ProcessEndTimestampForGtfsMetadata
from usecase.process_stops_count_by_type_for_gtfs_metadata import ProcessStopsCountByTypeForGtfsMetadata
from usecase.process_routes_count_by_type_for_gtfs_metadata import ProcessRoutesCountByTypeForGtfsMetadata
from usecase.process_agencies_count_for_gtfs_metadata import ProcessAgenciesCountForGtfsMetadata


def download_data(path_to_data, dataset_type="GTFS", specific_download=False, specific_entity_code=None):
    extract_sources_url = ExtractSourcesUrl(Managers.staging_api_request_manager(),
                                            Managers.staging_sparql_request_manager(),
                                            dataset_type, specific_download, specific_entity_code)
    urls = extract_sources_url.execute()
    download_dataset = DownloadDatasetAsZip(path_to_data, urls)
    return download_dataset.execute()


def process_data_md5(paths_to_datasets):
    entity_codes = list(paths_to_datasets.keys())
    extract_database_md5 = ExtractDatabaseMd5(Managers.staging_api_request_manager(),
                                              Managers.staging_sparql_request_manager(),
                                              entity_codes)
    previous_md5_hashes = extract_database_md5.execute()
    process_md5 = ProcessMd5(paths_to_datasets, previous_md5_hashes)
    return process_md5.execute()


def load_data(data_repository, dataset_representation_factory, datasets, data_type='GTFS'):
    load_dataset = LoadDataset(data_repository, dataset_representation_factory, datasets, data_type)
    return load_dataset.execute()


def compare_stops(dataset):
    compare_dataset_stops = CompareGtfsStops(dataset, dataset)
    compare_dataset_stops.execute()


def print_items_by_query(query):
    # Get all data from Wikibase image
    # Can be also use to get all related data to an entity,
    # i.e. all sub-entities of "Public transport operator", like STM, MBTA, etc.
    sparql_request_manager = Managers.staging_sparql_request_manager()
    sparql_response = sparql_request_manager.execute_get(query)
    results = []
    print(sparql_response)
    for result in sparql_response["results"]["bindings"]:
        print(result)
        print(result['a']['value'][37:40])
        results.append(result['a']['value'][37:40])

    # Get data for a specific entity from Wikibase image
    api_request_manager = Managers.staging_api_request_manager()
    for result in results:
        params = {
            "action": "wbgetentities",
            "ids": "%s" % result,
            "languages": "en",
            "format": "json"
        }
        api_request = api_request_manager.execute_get(params)
        print(api_request)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MobilityDatabase Interface Script')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--data_type', action='store', choices=['GTFS', 'GBFS'], default='GTFS',
                       help='Type of the datasets to process. Possible values : "GTFS", "GBFS".')
    group.add_argument('--download', action='store_const', const=True,
                       help='Download datasets in memory. Usage : --download (-a | -s SPECIFIC)')
    group.add_argument('--load', action='store', help='Load a dataset in memory. Must include path '
                                                      'to the dataset zip file as positional argument.')
    download_group = parser.add_mutually_exclusive_group(required='--download' in sys.argv)
    download_group.add_argument('-a', '--all', action='store_const', const=True,
                                help='Download all datasets found for a type in the Mobility Database.'
                                     'Required with --download to select the "Download all" option.')
    download_group.add_argument('-s', '--specific', action='store',
                                help='Download the dataset related to an entity code in the Mobility Database. '
                                     'Entity code for the specific dataset to download must be valid and provided '
                                     'as positional argument. Required with --download to select '
                                     'the "Download specific" option.')
    parser.add_argument('--path_to_tmp_data', action='store', default='./data/tmp/',
                        help='Path to the folder where to temporary store downloaded datasets for processing.')
    args = vars(parser.parse_args())

    # Initialize DataRepository
    data_repository = DataRepository()

    # Initialize DatasetRepresentationFactory
    dataset_representation_factory = DatasetRepresentationFactory()

    # Process data
    if args['download'] is not None:
        # Download datasets zip files
        if args['all'] is not None:
            paths_to_datasets = download_data(args['path_to_tmp_data'], dataset_type=args['data_type'])
        elif args['specific'] is not None:
            paths_to_datasets = download_data(args['path_to_tmp_data'], specific_download=True,
                                              specific_entity_code=args['specific'])

        # Process the MD5 hashes
        paths_to_datasets_and_md5 = process_data_md5(paths_to_datasets)

        # Load the datasets in memory in the data repository
        data_repository = load_data(data_repository,
                                    dataset_representation_factory,
                                    paths_to_datasets_and_md5,
                                    args['data_type'])

        # Process each dataset representation in the data_repository
        for dataset_key, dataset_representation in data_repository.get_dataset_representations().items():
            ProcessStartServiceDateForGtfsMetadata(dataset_representation).execute()
            ProcessEndServiceDateForGtfsMetadata(dataset_representation).execute()
            ProcessStartTimestampForGtfsMetadata(dataset_representation).execute()
            ProcessEndTimestampForGtfsMetadata(dataset_representation).execute()
            ProcessMainLanguageCodeForGtfsMetadata(dataset_representation).execute()
            ProcessMainTimezoneForGtfsMetadata(dataset_representation).execute()
            ProcessAllTimezonesForGtfsMetadata(dataset_representation).execute()
            ProcessBoundingBoxForGtfsMetadata(dataset_representation).execute()
            ProcessBoundingOctagonForGtfsMetadata(dataset_representation).execute()
            ProcessAgenciesCountForGtfsMetadata(dataset_representation).execute()
            ProcessRoutesCountByTypeForGtfsMetadata(dataset_representation).execute()
            ProcessStopsCountByTypeForGtfsMetadata(dataset_representation).execute()

            # Print results
            data_repository.print_dataset_representation(dataset_key)

    elif args['load'] is not None:
        # Load dataset in memory
        # TODO dataset = load_data(args['load'])
        pass

    # Print memory usage
    print("\n--------------- Memory Usage ---------------\n")
    print(hpy().heap())
