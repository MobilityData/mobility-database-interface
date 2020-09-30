from repository.gtfs_data_repository import GtfsDataRepository
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from usecase.compare_gtfs_stops import CompareGtfsStops

# Loads dataset in memory
data = GtfsDataRepository('../data/citcrc.zip')
data.display_dataset()
dataset = data.get_dataset()

# Compare dataset stops
compare_dataset_stops = CompareGtfsStops(dataset, dataset)
compare_dataset_stops.execute()

# Get all data from Wikibase image
# Can be also use to get all related data to an entity,
# i.e. all sub-entities of "Public transport operator", like STM, MBTA, etc.
sparql_request_manager = SparqlRequestManager()

#Get STM bus lines
query = """
SELECT *
WHERE 
{
  ?a 
  <http://wikibase.svc/prop/statement/P27>
  <http://wikibase.svc/entity/Q61>
}"""

sparql_request = sparql_request_manager.get_request(query)

results = []
for result in sparql_request["results"]["bindings"]:
    print(result)
    print(result['a']['value'][37:40])
    results.append(result['a']['value'][37:40])

# Get data for a specific entity from Wikibase image
api_request_manager = ApiRequestManager()

for result in results:
    params = {
        "action": "wbgetentities",
        "ids": "%s" % result,
        "languages": "en",
        "format": "json"
    }
    api_request = api_request_manager.get_request(params=params)
    print(api_request.json())
