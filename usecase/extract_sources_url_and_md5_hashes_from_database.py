from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_request_manager import SparqlRequestManager
from utilities.constant import GTFS_CATALOG_OF_SOURCES_CODE, GBFS_CATALOG_OF_SOURCES_CODE

OPEN_MOBILITY_DATA_URL = "openmobilitydata.org"

API_REQUEST_ACTION_KEY = "action"
API_REQUEST_ACTION_VALUE = "wbgetentities"
API_REQUEST_ID_KEY = "ids"
API_REQUEST_LANGUAGE_KEY = "languages"
API_REQUEST_LANGUAGE_VALUE = "en"
API_REQUEST_FORMAT_KEY = "format"
API_REQUEST_FORMAT_VALUE = "json"

API_ENTITIES_KEY = "entities"
API_CLAIMS_KEY = "claims"
API_STABLE_URL_PROPERTY_KEY = "P55"
API_MD5_HASH_KEY = "P61"
API_MAINSNAK_KEY = "mainsnak"
API_DATAVALUE_KEY = "datavalue"
API_VALUE_KEY = "value"

SPARQL_RESULTS_KEY = "results"
SPARQL_RESULT_CATEGORY_KEY = "bindings"
SPARQL_FIELD_KEY = "a"
SPARQL_VALUE_KEY = "value"
SPARQL_ENTITY_CODE_FIRST_INDEX = 37
SPARQL_ENTITY_CODE_LAST_INDEX = 40

SPARQL_CATALOG_REQUEST = "sparql_catalog_request"

GTFS_SOURCES_URL_MAP = {
    SPARQL_CATALOG_REQUEST:
        f"""
        SELECT *
        WHERE 
        {{
            ?a 
            <http://wikibase.svc/prop/statement/P65>
            <http://wikibase.svc/entity/{GTFS_CATALOG_OF_SOURCES_CODE}>
        }}""",
}

GBFS_SOURCES_URL_MAP = {
    SPARQL_CATALOG_REQUEST:
        f"""
        SELECT *
        WHERE 
        {{
            ?a 
            <http://wikibase.svc/prop/statement/P65>
            <http://wikibase.svc/entity/{GBFS_CATALOG_OF_SOURCES_CODE}>
        }}""",
}

SPARQL_SOURCE_REQUEST = (
    """
    SELECT *
    WHERE 
    {{
        ?a 
        <http://wikibase.svc/prop/statement/P65>
        <http://wikibase.svc/entity/{}>
    }}""")


def extract_gtfs_sources_url_and_md5_hashes_from_database(api_request_manager, sparql_request_manager):
    return extract_sources_url_and_md5_hashes_from_database(api_request_manager,
                                                            sparql_request_manager,
                                                            GTFS_SOURCES_URL_MAP)


def extract_gbfs_sources_url_and_md5_hashes_from_database(api_request_manager, sparql_request_manager):
    return extract_sources_url_and_md5_hashes_from_database(api_request_manager,
                                                            sparql_request_manager,
                                                            GBFS_SOURCES_URL_MAP)


def extract_sources_url_and_md5_hashes_from_database(api_request_manager, sparql_request_manager, data_type_map):
    """ Extract the stable URLs and MD5 hashes from previous dataset versions
    for each dataset of a data type in the database.
    :param api_request_manager: API request manager used to process API requests.
    :param sparql_request_manager: SPARQL request manager used to process SPARQL queries.
    :param data_type_map: Either SOURCES_URL_MAP or MD5_HASHES_MAP.
    :return: the URLs and MD5 hashes for each dataset of a data type in the database.
    """
    if not isinstance(api_request_manager, ApiRequestManager):
        raise TypeError("API request manager must be a valid ApiRequestManager.")
    if not isinstance(sparql_request_manager, SparqlRequestManager):
        raise TypeError("SPARQL request manager must be a valid SparqlRequestManager.")
    entity_codes = []
    urls = {}
    previous_md5_hashes = {}

    # Retrieves the entity codes for which we want to download the dataset
    sparql_response = sparql_request_manager.execute_get(data_type_map[SPARQL_CATALOG_REQUEST])

    for result in sparql_response[SPARQL_RESULTS_KEY][SPARQL_RESULT_CATEGORY_KEY]:
        entity_codes.append(result[SPARQL_FIELD_KEY][SPARQL_VALUE_KEY][SPARQL_ENTITY_CODE_FIRST_INDEX:
                                                                       SPARQL_ENTITY_CODE_LAST_INDEX])

    # Retrieves the sources' stable URL for the entity codes found
    for entity_code in entity_codes:
        urls[entity_code] = extract_source_url(api_request_manager,
                                               entity_code)
        previous_md5_hashes[entity_code] = extract_md5_hashes(api_request_manager,
                                                              sparql_request_manager,
                                                              entity_code)

    return urls, previous_md5_hashes


def extract_md5_hashes(api_request_manager, sparql_request_manager, entity_code):
    dataset_version_codes = set()
    entity_previous_md5_hashes = set()

    # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
    sparql_response = sparql_request_manager.execute_get(SPARQL_SOURCE_REQUEST.format(entity_code))

    for result in sparql_response[SPARQL_RESULTS_KEY][SPARQL_RESULT_CATEGORY_KEY]:
        dataset_version_codes.add(result[SPARQL_FIELD_KEY][SPARQL_VALUE_KEY][SPARQL_ENTITY_CODE_FIRST_INDEX:
                                                                             SPARQL_ENTITY_CODE_LAST_INDEX])

    # Verify if entity if part of a catalog of sources.
    # If yes, removes the catalog of sources entity code, which appears in the results of a source entity,
    # and initialize entity element in the MD5 hashes dictionary. This operation makes sure that an entity
    # with no MD5 hash in the database, but in a catalog of sources, gets initialized with an empty set
    # in the MD5 hashes dictionary (required for further MD5 processing).
    if (GTFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes or
            GBFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes):

        dataset_version_codes.discard(GTFS_CATALOG_OF_SOURCES_CODE)
        dataset_version_codes.discard(GBFS_CATALOG_OF_SOURCES_CODE)

    # Retrieves the MD5 hashes for the dataset version codes found.
    for version_code in dataset_version_codes:
        api_response = execute_api_get_request(api_request_manager, version_code)

        if API_ENTITIES_KEY in api_response:
            for row in api_response[API_ENTITIES_KEY][version_code][API_CLAIMS_KEY][API_MD5_HASH_KEY]:
                md5 = row[API_MAINSNAK_KEY][API_DATAVALUE_KEY][API_VALUE_KEY]
                entity_previous_md5_hashes.add(md5)

    return entity_previous_md5_hashes


def extract_source_url(api_request_manager, entity_code):
    api_response = execute_api_get_request(api_request_manager, entity_code)

    url = None
    if API_ENTITIES_KEY in api_response:
        for link in api_response[API_ENTITIES_KEY][entity_code][API_CLAIMS_KEY][API_STABLE_URL_PROPERTY_KEY]:
            if OPEN_MOBILITY_DATA_URL not in link[API_MAINSNAK_KEY][API_DATAVALUE_KEY][API_VALUE_KEY]:
                url = link[API_MAINSNAK_KEY][API_DATAVALUE_KEY][API_VALUE_KEY]

    return url


def execute_api_get_request(api_request_manager, entity_code):
    params = {
        API_REQUEST_ACTION_KEY: API_REQUEST_ACTION_VALUE,
        API_REQUEST_ID_KEY: entity_code,
        API_REQUEST_LANGUAGE_KEY: API_REQUEST_LANGUAGE_VALUE,
        API_REQUEST_FORMAT_KEY: API_REQUEST_FORMAT_VALUE
    }
    return api_request_manager.execute_get(params)
