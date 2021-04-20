import os
from representation.dataset_infos import DatasetInfos
from utilities.constants import (
    VALUE,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    LABELS,
    ENGLISH,
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    SHA1_HASH_PROP,
    STABLE_URL_PROP,
)
from utilities.request_utils import (
    extract_dataset_version_codes,
    extract_source_entity_codes,
    wbi_core,
)
from utilities.validators import validate_api_url, validate_sparql_url

OPEN_MOBILITY_DATA_URL = "openmobilitydata.org"


def extract_gtfs_datasets_infos_from_database(api_url, sparql_api):
    return extract_datasets_infos_from_database(
        api_url, sparql_api, os.environ[GTFS_CATALOG_OF_SOURCES_CODE]
    )


def extract_gbfs_datasets_infos_from_database(api_url, sparql_api):
    return extract_datasets_infos_from_database(
        api_url, sparql_api, os.environ[GBFS_CATALOG_OF_SOURCES_CODE]
    )


def extract_datasets_infos_from_database(api_url, sparql_api, catalog_code):
    """Extract the stable URLs and MD5 hashes from previous dataset versions
    for each dataset of a data type in the database.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :param sparql_api: SPARQL api, either PRODUCTION_SPARQL_URL or STAGING_SPARQL_URL.
    :param catalog_code: Either GTFS_CATALOG_OF_SOURCES_CODE or GBFS_CATALOG_OF_SOURCES_CODE.
    :return: A list of DatasetInfos, each containing the URL and SHA-1 hashes of a dataset in the database.
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

        dataset_infos.previous_sha1_hashes = extract_previous_sha1_hashes(entity_code)

        datasets_infos.append(dataset_infos)

    return datasets_infos


def extract_previous_sha1_hashes(entity_code):
    entity_previous_sha1_hashes = set()
    entity_sha1_hashes = set()

    # Retrieves the entity dataset version codes for which we want to extract the SHA-1 hashes.
    dataset_version_codes = extract_dataset_version_codes(entity_code)

    # Retrieves the SHA-1 hashes for the dataset version codes found.
    for version_code in dataset_version_codes:
        # Export entity related to the version code from database
        json_response = wbi_core.ItemEngine(
            item_id=version_code
        ).get_json_representation()

        for row in json_response.get(CLAIMS, {}).get(os.environ[SHA1_HASH_PROP], []):
            sha1 = row.get(MAINSNAK, {}).get(DATAVALUE, {}).get(VALUE)
            if sha1 is None:
                continue
            entity_sha1_hashes.add(sha1)
        # Add the SHA-1 hashes found for an entity to the SHA-1 hashes dictionary.
        entity_previous_sha1_hashes.update(entity_sha1_hashes)

    return entity_previous_sha1_hashes


def extract_source_infos(entity_code):
    # Export entity related to the entity code from database
    json_response = wbi_core.ItemEngine(item_id=entity_code).get_json_representation()

    url = None
    # Extract source stable URL
    for link in json_response.get(CLAIMS, {}).get(os.environ[STABLE_URL_PROP], []):
        tmp_url = link.get(MAINSNAK, {}).get(DATAVALUE, {}).get(VALUE)
        if OPEN_MOBILITY_DATA_URL not in tmp_url:
            url = tmp_url

    name = json_response.get(LABELS, {}).get(ENGLISH, {}).get(VALUE)

    return url, name
