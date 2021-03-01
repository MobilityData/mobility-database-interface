import requests
import re

from request_manager.sparql_request_helper import sparql_request
from representation.dataset_infos import DatasetInfos
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    RESULTS,
    BINDINGS,
    VALUE,
    SPARQL_ENTITY_CODE_REGEX,
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
    ID,
)
from utilities.request_utils import extract_dataset_version_codes
from utilities.validators import validate_api_url, validate_sparql_url

OPEN_MOBILITY_DATA_URL = "openmobilitydata.org"
API_STABLE_URL_PROPERTY_KEY = "P55"
API_MD5_HASH_KEY = "P61"
API_PREVIOUS_VERSIONS_KEY = "P64"


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
            re.search(SPARQL_ENTITY_CODE_REGEX, result["a"][VALUE]).group(1)
        )

    # Retrieves the sources' stable URL for the entity codes found
    for entity_code in entity_codes:

        dataset_infos = DatasetInfos()
        dataset_infos.entity_code = entity_code

        url, name, previous_versions = extract_source_infos(api_url, entity_code)
        if not url or not name:
            continue
        dataset_infos.url = url
        dataset_infos.source_name = name
        dataset_infos.previous_versions = previous_versions

        dataset_infos.previous_md5_hashes = extract_previous_md5_hashes(
            api_url, sparql_api, entity_code
        )

        datasets_infos.append(dataset_infos)

    return datasets_infos


def extract_previous_md5_hashes(api_url, sparql_api, entity_code):
    entity_previous_md5_hashes = set()
    entity_md5_hashes = set()

    # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
    dataset_version_codes = extract_dataset_version_codes(entity_code, sparql_api)

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


def extract_source_infos(api_url, entity_code):
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
    previous_versions = set()
    if not ENTITIES in json_response:
        return None

    # Extract source stable URL
    for link in json_response[ENTITIES][entity_code][CLAIMS][
        API_STABLE_URL_PROPERTY_KEY
    ]:
        if OPEN_MOBILITY_DATA_URL not in link[MAINSNAK][DATAVALUE][VALUE]:
            url = link[MAINSNAK][DATAVALUE][VALUE]

    # Extract source name
    name = json_response[ENTITIES][entity_code][LABELS][ENGLISH][VALUE]

    # Extract the codes of the source previous dataset versions
    if API_PREVIOUS_VERSIONS_KEY in json_response[ENTITIES][entity_code][CLAIMS]:
        for version in json_response[ENTITIES][entity_code][CLAIMS][
            API_PREVIOUS_VERSIONS_KEY
        ]:
            previous_versions.add(version[MAINSNAK][DATAVALUE][VALUE][ID])

    return url, name, previous_versions
