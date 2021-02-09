from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from utilities.constant import GTFS_CATALOG_OF_SOURCES, GBFS_CATALOG_OF_SOURCES


class ExtractDatabaseMd5:
    # Define index values for dataset version entity code in response retrieved by SPARQL query
    DATASET_VERSION_ENTITY_CODE_FIRST_INDEX = 37
    DATASET_VERSION_ENTITY_CODE_LAST_INDEX = 40

    def __init__(self, api_request_manager, sparql_request_manager, entity_codes):
        """Constructor for ``ExtractDatabaseMd5``.
        :param api_request_manager: API request manager used to process API requests.
        :param sparql_request_manager: SPARQL request manager used to process SPARQL queries.
        :param entity_codes: The entity codes of the entities for which to extract the MD5 hashes from the database.
        One MD5 hash exists per dataset version of each entity.
        """
        try:
            if api_request_manager is None or not isinstance(
                api_request_manager, ApiRequestManager
            ):
                raise TypeError(
                    "API request manager must be a valid ApiRequestManager."
                )
            self.api_request_manager = api_request_manager
            if sparql_request_manager is None or not isinstance(
                sparql_request_manager, SparqlRequestManager
            ):
                raise TypeError(
                    "SPARQL request manager must be a valid SparqlRequestManager."
                )
            self.sparql_request_manager = sparql_request_manager
            if entity_codes is None or not isinstance(entity_codes, list):
                raise TypeError("Entity codes must be a valid entity codes list.")
            self.entity_codes = entity_codes
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ExtractDatabaseMd5`` use case. Extract the MD5 hashes from the database.
        :return: The MD5 hashes of the dataset versions in the database, for the entities associated
        to the `entity_codes` passed in the constructor.
        """
        previous_md5_hashes = {}

        # Iterate over the entities using their entity codes in the database.
        for entity_code in self.entity_codes:
            dataset_version_codes = set()
            entity_md5_hashes = set()

            # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
            sparql_response = self.sparql_request_manager.execute_get(
                """
                SELECT *
                WHERE 
                {
                    ?a 
                    <http://wikibase.svc/prop/statement/P48>
                    <http://wikibase.svc/entity/%s>
                }"""
                % entity_code
            )

            for result in sparql_response["results"]["bindings"]:
                dataset_version_codes.add(
                    result["a"]["value"][
                        self.DATASET_VERSION_ENTITY_CODE_FIRST_INDEX : self.DATASET_VERSION_ENTITY_CODE_LAST_INDEX
                    ]
                )

            # Verify if entity if part of a catalog of sources.
            # If yes, removes the catalog of sources entity code, which appears in the results of a source entity,
            # and initialize entity element in the MD5 hashes dictionary. This operation makes sure that an entity
            # with no MD5 hash in the database, but in a catalog of sources, gets initialized with an empty set
            # in the MD5 hashes dictionary (required for further MD5 processing).
            if (
                GTFS_CATALOG_OF_SOURCES in dataset_version_codes
                or GBFS_CATALOG_OF_SOURCES in dataset_version_codes
            ):

                dataset_version_codes.discard(GTFS_CATALOG_OF_SOURCES)
                dataset_version_codes.discard(GBFS_CATALOG_OF_SOURCES)
                previous_md5_hashes[entity_code] = set()

            # Retrieves the MD5 hashes for the dataset version codes found.
            for version_code in dataset_version_codes:
                params = {
                    "action": "wbgetentities",
                    "ids": "%s" % version_code,
                    "languages": "en",
                    "format": "json",
                }
                api_response = self.api_request_manager.execute_get(params)

                if "entities" in api_response:
                    for row in api_response["entities"][version_code]["claims"]["P61"]:
                        md5 = row["mainsnak"]["datavalue"]["value"]
                        entity_md5_hashes.add(md5)
                    # Add the MD5 hashes found for an entity to the MD5 hashes dictionary.
                    previous_md5_hashes[entity_code].update(entity_md5_hashes)

        return previous_md5_hashes
