import requests

from request_manager.sparql_request_helper import sparql_request
from representation.dataset_infos import DatasetInfos
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    RESULTS,
    BINDINGS,
    VALUE,
    DATASET_VERSION_ENTITY_CODE_FIRST_INDEX,
    DATASET_VERSION_ENTITY_CODE_LAST_INDEX,
    ACTION,
    WB_GET_ENTITIES,
    IDS,
    LANGUAGES,
    FORMAT,
    ENTITIES,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    LABELS,
    ENGLISH,
)
from utilities.validators import validate_api_url, validate_sparql_url

OPEN_MOBILITY_DATA_URL = "openmobilitydata.org"
API_STABLE_URL_PROPERTY_KEY = "P55"
API_MD5_HASH_KEY = "P61"


def extract_gtfs_datasets_infos_from_database(api_url, sparql_api):
    return extract_datasets_infos_from_database(
        api_url, sparql_api, GTFS_CATALOG_OF_SOURCES_CODE
    )


def extract_gbfs_datasets_infos_from_database(api_url, sparql_api):
    return extract_datasets_infos_from_database(
        api_url, sparql_api, GBFS_CATALOG_OF_SOURCES_CODE
    )


def extract_datasets_infos_from_database(api_url, sparql_api, catalog_code):
    """Extract the stable URLs and MD5 hashes from previous dataset versions
    for each dataset of a data type in the database.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :param sparql_api: SPARQL api, either PRODUCTION_SPARQL_URL or STAGING_SPARQL_URL.
    :param catalog_code: Either GTFS_CATALOG_OF_SOURCES_CODE or GBFS_CATALOG_OF_SOURCES_CODE.
    :return: A list of DatasetInfos, each containing the URL and MD5 hashes of a dataset in the database.
    """
    validate_api_url(api_url)
    validate_sparql_url(sparql_api)
    entity_codes = []
    datasets_infos = []

    # Retrieves the entity codes for which we want to download the dataset
    sparql_response = sparql_request(
        sparql_api,
        f"""
            SELECT *
            WHERE 
            {{
                ?a 
                <http://wikibase.svc/prop/statement/P65>
                <http://wikibase.svc/entity/{catalog_code}>
            }}""",  # double curly bracket escapes a curly bracket
    )

    for result in sparql_response[RESULTS][BINDINGS]:
        entity_codes.append(
            result["a"][VALUE][
                DATASET_VERSION_ENTITY_CODE_FIRST_INDEX:DATASET_VERSION_ENTITY_CODE_LAST_INDEX
            ]
        )

    # Retrieves the sources' stable URL for the entity codes found
    for entity_code in entity_codes:

        dataset_infos = DatasetInfos()
        dataset_infos.entity_code = entity_code

        url, name = extract_source_url_and_name(api_url, entity_code)
        if not url or not name:
            continue
        dataset_infos.url = url
        dataset_infos.source_name = name

        dataset_infos.previous_md5_hashes = extract_previous_md5_hashes(
            api_url, sparql_api, entity_code
        )

        datasets_infos.append(dataset_infos)

    return datasets_infos


def extract_previous_md5_hashes(api_url, sparql_api, entity_code):
    dataset_version_codes = set()
    entity_previous_md5_hashes = set()
    entity_md5_hashes = set()

    # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
    sparql_response = sparql_request(
        sparql_api,
        f"""
                SELECT *
                WHERE 
                {{
                    ?a 
                    <http://wikibase.svc/prop/statement/P48>
                    <http://wikibase.svc/entity/{entity_code}>
                }}""",
    )

    for result in sparql_response[RESULTS][BINDINGS]:
        dataset_version_codes.add(
            result["a"][VALUE][
                DATASET_VERSION_ENTITY_CODE_FIRST_INDEX:DATASET_VERSION_ENTITY_CODE_LAST_INDEX
            ]
        )

    # Verify if entity if part of a catalog of sources.
    # If yes, removes the catalog of sources entity code, which appears in the results of a source entity,
    # and initialize entity element in the MD5 hashes dictionary. This operation makes sure that an entity
    # with no MD5 hash in the database, but in a catalog of sources, gets initialized with an empty set
    # in the MD5 hashes dictionary (required for further MD5 processing).
    if (
        GTFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes
        or GBFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes
    ):
        dataset_version_codes.discard(GTFS_CATALOG_OF_SOURCES_CODE)
        dataset_version_codes.discard(GBFS_CATALOG_OF_SOURCES_CODE)

    # Retrieves the MD5 hashes for the dataset version codes found.
    for version_code in dataset_version_codes:
        params = {
            ACTION: WB_GET_ENTITIES,
            IDS: f"{version_code}",
            LANGUAGES: "en",
            FORMAT: "json",
        }
        api_response = requests.get(api_url, params)
        api_response.raise_for_status()
        json_response = api_response.json()
        if ENTITIES not in json_response:
            continue
        for row in json_response[ENTITIES][version_code][CLAIMS][API_MD5_HASH_KEY]:
            md5 = row[MAINSNAK][DATAVALUE][VALUE]
            entity_md5_hashes.add(md5)
        # Add the MD5 hashes found for an entity to the MD5 hashes dictionary.
        entity_previous_md5_hashes.update(entity_md5_hashes)
    return entity_previous_md5_hashes


def extract_source_url_and_name(api_url, entity_code):
    params = {
        ACTION: WB_GET_ENTITIES,
        IDS: f"{entity_code}",
        LANGUAGES: "en",
        FORMAT: "json",
    }
    api_response = requests.get(api_url, params)
    api_response.raise_for_status()
    json_response = api_response.json()

    url = None
    name = None
    if not ENTITIES in json_response:
        return None

    for link in json_response[ENTITIES][entity_code][CLAIMS][
        API_STABLE_URL_PROPERTY_KEY
    ]:
        if OPEN_MOBILITY_DATA_URL not in link[MAINSNAK][DATAVALUE][VALUE]:
            url = link[MAINSNAK][DATAVALUE][VALUE]

    name = json_response[ENTITIES][entity_code][LABELS][ENGLISH][VALUE]

    return url, name
