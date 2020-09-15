from repository.gtfs_data_repository import GtfsDataRepository
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from usecase.compare_gtfs_stops import CompareGtfsStops

# Loads feed in memory
data = GtfsDataRepository('citcrc.zip')
data.display_feed()
feed = data.get_feed()

# Compare feeds' stops
compare_feeds_stops = CompareGtfsStops(feed, feed)
compare_feeds_stops.execute()

# Get data for a specific entity from Wikibase image
api_request_manager = ApiRequestManager()

params = {
    "action": "wbgetentities",
    "ids": "Q57",
    "languages": "en",
    "format": "json"
}

api_request = api_request_manager.get_request(params=params)
print(api_request.json())

# Get all data from Wikibase image
# Can be also use to get all related data to an entity,
# i.e. all sub-entities of "Public transport operator", like STM, MBTA, etc.
sparql_request_manager = SparqlRequestManager()

query_wikidata = """
SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q178512.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""

query_mobility_database = """
SELECT *
WHERE 
{
  ?a ?b ?c
}"""

sparql_request = sparql_request_manager.get_request(query_mobility_database)

for result in sparql_request["results"]["bindings"]:
    print(result)
