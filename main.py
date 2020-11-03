import argparse
import sys
from guppy import hpy
from repository.gtfs_data_repository import GtfsDataRepository
from request_manager.request_manager_containers import Managers
from usecase.compare_gtfs_stops import CompareGtfsStops
from usecase.download_dataset import DownloadDataset
from usecase.extract_sources_url import ExtractSourcesUrl
from usecase.extract_database_md5 import ExtractDatabaseMd5


def load_dataset(dataset_path):
    data = GtfsDataRepository()
    data.add_dataset("test", dataset_path)
    data.display_dataset("test")
    return data.get_datasets()


def download_data(data_folder_path, dataset_type="GTFS", specific_download=False, specific_entity_code=None):
    extract_sources_url = ExtractSourcesUrl(Managers.staging_api_request_manager(),
                                            Managers.staging_sparql_request_manager(),
                                            dataset_type, specific_download, specific_entity_code)
    urls = extract_sources_url.execute()
    download_dataset = DownloadDataset(data_folder_path, urls)
    datasets = download_dataset.execute()
    return datasets


def process_data_md5(datasets):
    entity_codes = list(datasets.keys())
    extract_database_md5 = ExtractDatabaseMd5(Managers.staging_api_request_manager(),
                                              Managers.staging_sparql_request_manager(),
                                              entity_codes)
    database_md5 = extract_database_md5.execute()
    print(database_md5)


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
    group.add_argument('--download', action='store_const', const=True, help='Download datasets in memory')
    group.add_argument('--load', action='store', help='Load a dataset in memory. Must include path '
                                                      'to the dataset zip file as positional argument.')
    download_group = parser.add_mutually_exclusive_group(required='--download' in sys.argv)
    download_group.add_argument('-a', '--all', action='store', choices=['GTFS','GBFS'],
                                help='Download all datasets found for a type in the Mobility Database. '
                                     'The datasets type must be provided as positional argument.'
                                     'Possible values : "GTFS", "GBFS".')
    download_group.add_argument('-s', '--specific', action='store',
                                help='Download the dataset related to an entity code in the Mobility Database. '
                                     'Entity code for the specific dataset to download must be valid and provided '
                                     'as positional argument.')
    download_group.add_argument('--tmp_data_folder_path', action='store', default='./data/tmp/',
                                help='Path to the folder where to temporary store downloaded datasets for processing.')
    args = vars(parser.parse_args())

    # Initialise GtfsDataRepository
    gtfs_data_repository = GtfsDataRepository()

    if args['download'] is not None:
        # Download datasets in memory
        if args['all'] is not None:
            data = download_data(args['tmp_data_folder_path'], dataset_type=args['all'])
        elif args['specific'] is not None:
            data = download_data(args['tmp_data_folder_path'], specific_download=True,
                                 specific_entity_code=args['specific'])
        process_data_md5(data)
    elif args['load'] is not None:
        # Load dataset in memory
        dataset = load_dataset(args['load'])


    # Compare dataset stops
    #compare_stops(dataset)

    # Query for all data
    query_all = """
    SELECT *
    WHERE
    {
      ?a
      ?b
      ?c
    }"""

    # Query for STM bus lines
    query_stm = """
    SELECT *
    WHERE
    {
      ?a
      <http://wikibase.svc/prop/statement/P27>
      <http://wikibase.svc/entity/Q61>
    }"""

    # Print items for the requested query
    #print_items_by_query(query_stm)

    # Print memory usage
    print("\n--------------- Memory Usage ---------------\n")
    print(hpy().heap())
