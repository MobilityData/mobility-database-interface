import argparse
from repository.gtfs_data_repository import GtfsDataRepository
from request_manager.request_manager_containers import Configs, Managers
from usecase.compare_gtfs_stops import CompareGtfsStops
from utilities import external_utils


def load_dataset(dataset_path):
    data = GtfsDataRepository(dataset_path)
    data.display_dataset()
    return data.get_dataset()


def compare_dataset_stops(dataset):
    compare_dataset_stops = CompareGtfsStops(dataset, dataset)
    compare_dataset_stops.execute()


def print_items_by_query(query):
    # Get all data from Wikibase image
    # Can be also use to get all related data to an entity,
    # i.e. all sub-entities of "Public transport operator", like STM, MBTA, etc.
    sparql_request_manager = Managers.staging_sparql_request_manager()
    sparql_response = sparql_request_manager.execute_get(query)
    results = []
    for result in sparql_response["results"]["bindings"]:
        #print(result)
        #print(result['a']['value'][37:40])
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
        api_request = api_request_manager.execute_get(params=params)
        print(api_request)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MobilityDatabase Interface Script')
    parser.add_argument('-d', '--dataset_path', action='store', dest='dataset_path', required=True,
                        help='Path to the GTFS dataset zip to verify')
    args = vars(parser.parse_args())

    # Loads dataset in memory
    dataset = load_dataset(args['dataset_path'])

    # Compare dataset stops
    compare_dataset_stops(dataset)

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
    print_items_by_query(query_stm)
