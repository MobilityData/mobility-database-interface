from gtfs_data_repository import GtfsDataRepository
from api_request_manager import ApiRequestManager

# Loads feed in memory
data = GtfsDataRepository('citcrc.zip')
data.display_feed()

# Get data from Wikidata
request_manager = ApiRequestManager()

params = {
    "action": "wbgetentities",
    "sites": "enwiki",
    "ids": "Q1817151",
    "props": "descriptions",
    "languages": "en",
    "format": "json"
}

request = request_manager.get_request(params=params)
print(request.json())

