from utilities.entities_codes import EntitiesCodes
import gtfs_kit as gtfs_kit


class DownloadDataset:
    def __init__(self, api_request_manager, sparql_request_manager, dataset_type="GTFS", specific_download=False,
                 specific_entity_code=None):
        self.api_request_manager = api_request_manager
        self.sparql_request_manager = sparql_request_manager

        if dataset_type == "GTFS":
            self.catalog_code = EntitiesCodes.GTFS_CATALOG_OF_SOURCES.value
        elif dataset_type == "GBFS":
            self.catalog_code = EntitiesCodes.GBFS_CATALOG_OF_SOURCES.value

        self.specific_download = specific_download
        self.specific_entity_code = specific_entity_code

    def get_urls_from_database(self):
        entity_codes = []
        urls = []

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

            for link in api_response["entities"][entity_code]["claims"]["P55"]:
                if "openmobilitydata.org" not in link["mainsnak"]["datavalue"]["value"]:
                    urls.append(link["mainsnak"]["datavalue"]["value"])

        return urls

    def execute(self):
        urls = self.get_urls_from_database()
        for url in urls:
            try:
                print("--------------- URL : %s ---------------\n" % url)
                dataset = gtfs_kit.read_feed(url, dist_units='km')
                print(dataset)
            except Exception as e:
                print("Problem occurred when opening URL\n")
