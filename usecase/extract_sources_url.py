from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from utilities.entities_codes import EntitiesCodes


class ExtractSourcesUrl:
    def __init__(self, api_request_manager, sparql_request_manager, dataset_type="GTFS", specific_download=False,
                 specific_entity_code=None):
        try:
            if api_request_manager is None or not isinstance(api_request_manager, ApiRequestManager):
                raise TypeError("API request manager must be a valid ApiRequestManager.")
            self.api_request_manager = api_request_manager
            if sparql_request_manager is None or not isinstance(sparql_request_manager, SparqlRequestManager):
                raise TypeError("SPARQL request manager must be a valid SparqlRequestManager.")
            self.sparql_request_manager = sparql_request_manager

            if dataset_type == "GTFS":
                self.catalog_code = EntitiesCodes.GTFS_CATALOG_OF_SOURCES.value
            elif dataset_type == "GBFS":
                self.catalog_code = EntitiesCodes.GBFS_CATALOG_OF_SOURCES.value

            self.specific_download = specific_download
            self.specific_entity_code = specific_entity_code
        except Exception as e:
            raise e

    def execute(self):
        entity_codes = []
        urls = {}

        # Retrieves the entity codes for which we want to download the dataset
        if not self.specific_download:
            sparql_response = self.sparql_request_manager.execute_get(
                """
                SELECT *
                WHERE 
                {
                    ?a 
                    <http://wikibase.svc/prop/statement/P65>
                    <http://wikibase.svc/entity/%s>
                }""" % self.catalog_code
            )

            for result in sparql_response["results"]["bindings"]:
                entity_codes.append(result['a']['value'][37:40])
        else:
            entity_codes.append(self.specific_entity_code)

        # Retrieves the sources' stable URL for the entity codes found
        for entity_code in entity_codes:
            params = {
                "action": "wbgetentities",
                "ids": "%s" % entity_code,
                "languages": "en",
                "format": "json"
            }
            api_response = self.api_request_manager.execute_get(params)

            if "entities" in api_response:
                for link in api_response["entities"][entity_code]["claims"]["P55"]:
                    if "openmobilitydata.org" not in link["mainsnak"]["datavalue"]["value"]:
                        urls[entity_code] = link["mainsnak"]["datavalue"]["value"]

        return urls
