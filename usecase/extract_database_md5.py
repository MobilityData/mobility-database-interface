import requests
from request_manager.sparql_request_helper import sparql_request
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES, GBFS_CATALOG_OF_SOURCES,
    DATASET_VERSION_ENTITY_CODE_FIRST_INDEX,
    DATASET_VERSION_ENTITY_CODE_LAST_INDEX,
    ACTION, IDS, FORMAT, LANGUAGES,
    ENTITIES, CLAIMS, MAINSNAK, DATAVALUE,
    VALUE, WB_GET_ENTITIES, RESULTS, BINDINGS,
    PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL,
    PRODUCTION_API_URL,
    STAGING_API_URL
)
from utilities.validators import validate_urls


def extract_database_md5(api_url, sparql_api, entity_codes):
    """Extract the MD5 hashes from the database.
    :param api_url: either STAGING_API_URL or PRODUCTION_API_URL in utilities/constants.py
    :param sparql_api: either STAGING_SPARQL_URL or PRODUCTION_SPARQL_URL in utilities/constants.py
    :param entity_codes: The entity codes of the entities for which to extract the MD5 hashes from the database.
    One MD5 hash exists per dataset version of each entity.
    :return: The MD5 hashes of the dataset versions in the database, for the entities associated
    to the `entity_codes` passed in the constructor.
    """
    validate_urls(api_url, sparql_api)

    if not isinstance(entity_codes, list):
        raise TypeError("Entity codes must be a valid entity codes list.")

    previous_md5_hashes = {}

    # Iterate over the entities using their entity codes in the database.
    for entity_code in entity_codes:
        dataset_version_codes = set()
        entity_md5_hashes = set()

        # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
        sparql_response = sparql_request(sparql_api,
            f"""
            SELECT *
            WHERE 
            {{
                ?a 
                <http://wikibase.svc/prop/statement/P48>
                <http://wikibase.svc/entity/{entity_code}>
            }}"""
        )

        for result in sparql_response[RESULTS][BINDINGS]:
            dataset_version_codes.add(
                result['a'][VALUE][DATASET_VERSION_ENTITY_CODE_FIRST_INDEX:DATASET_VERSION_ENTITY_CODE_LAST_INDEX])

        # Verify if entity if part of a catalog of sources.
        # If yes, removes the catalog of sources entity code, which appears in the results of a source entity,
        # and initialize entity element in the MD5 hashes dictionary. This operation makes sure that an entity
        # with no MD5 hash in the database, but in a catalog of sources, gets initialized with an empty set
        # in the MD5 hashes dictionary (required for further MD5 processing).
        if (GTFS_CATALOG_OF_SOURCES in dataset_version_codes or
            GBFS_CATALOG_OF_SOURCES in dataset_version_codes):

            dataset_version_codes.discard(GTFS_CATALOG_OF_SOURCES)
            dataset_version_codes.discard(GBFS_CATALOG_OF_SOURCES)
            previous_md5_hashes[entity_code] = set()

        # Retrieves the MD5 hashes for the dataset version codes found.
        for version_code in dataset_version_codes:
            params = {
                ACTION: WB_GET_ENTITIES,
                IDS: f"{version_code}",
                LANGUAGES: "en",
                FORMAT: "json"
            }
            api_response = requests.get(api_url, params)
            api_response.raise_for_status()
            json_response = api_response.json()
            if ENTITIES not in json_response:
                continue
            for row in json_response[ENTITIES][version_code][CLAIMS]["P61"]:
                md5 = row[MAINSNAK][DATAVALUE][VALUE]
                entity_md5_hashes.add(md5)
            # Add the MD5 hashes found for an entity to the MD5 hashes dictionary.
            previous_md5_hashes[entity_code].update(entity_md5_hashes)

    return previous_md5_hashes
