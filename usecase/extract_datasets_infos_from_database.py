from representation.dataset_infos import DatasetInfos
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    VALUE,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    LABELS,
    ENGLISH,
)
from utilities.request_utils import (
    extract_dataset_version_codes,
    extract_source_entity_codes,
    export_entity_as_json,
)
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
    datasets_infos = []

    entity_codes = extract_source_entity_codes(catalog_code)
    # Retrieves the sources' stable URL for the entity codes found
    for entity_code in entity_codes:

        dataset_infos = DatasetInfos()
        dataset_infos.entity_code = entity_code

        url, name = extract_source_infos(entity_code)
        if not url or not name:
            continue
        dataset_infos.url = url
        dataset_infos.source_name = name

        dataset_infos.previous_md5_hashes = extract_previous_md5_hashes(entity_code)

        datasets_infos.append(dataset_infos)

    return datasets_infos


def extract_previous_md5_hashes(entity_code):
    entity_previous_md5_hashes = set()
    entity_md5_hashes = set()

    # Retrieves the entity dataset version codes for which we want to extract the MD5 hashes.
    dataset_version_codes = extract_dataset_version_codes(entity_code)

    # Retrieves the MD5 hashes for the dataset version codes found.
    for version_code in dataset_version_codes:
        # Export entity related to the version code from database
        json_response = export_entity_as_json(version_code)

        if API_MD5_HASH_KEY not in json_response[CLAIMS]:
            continue
        for row in json_response[CLAIMS][API_MD5_HASH_KEY]:
            md5 = row[MAINSNAK][DATAVALUE][VALUE]
            entity_md5_hashes.add(md5)
        # Add the MD5 hashes found for an entity to the MD5 hashes dictionary.
        entity_previous_md5_hashes.update(entity_md5_hashes)

    return entity_previous_md5_hashes


def extract_source_infos(entity_code):
    # Export entity related to the entity code from database
    json_response = export_entity_as_json(entity_code)

    url = None
    if CLAIMS in json_response and API_STABLE_URL_PROPERTY_KEY in json_response[CLAIMS]:
        # Extract source stable URL
        for link in json_response[CLAIMS][API_STABLE_URL_PROPERTY_KEY]:
            if OPEN_MOBILITY_DATA_URL not in link[MAINSNAK][DATAVALUE][VALUE]:
                url = link[MAINSNAK][DATAVALUE][VALUE]

    name = None
    if LABELS in json_response:
        # Extract source name
        name = json_response[LABELS][ENGLISH][VALUE]

    return url, name
