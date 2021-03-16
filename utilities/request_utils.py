import re

from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    RESULTS,
    BINDINGS,
    VALUE,
    SPARQL_ENTITY_CODE_REGEX,
    ENGLISH,
    DATATYPE,
    RANK,
    PROP_ID,
    IF_EXISTS,
    SPARQL_A,
    SVC_SOURCE_PROPERTY_URL,
    SVC_ENTITY_URL_PREFIX,
    SVC_CATALOG_PROPERTY_URL,
)

from wikibaseintegrator import wbi_core, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
from utilities.constants import STAGING_API_URL, STAGING_SPARQL_BIGDATA_URL, SVC_URL

wbi_config["MEDIAWIKI_API_URL"] = STAGING_API_URL
wbi_config["SPARQL_ENDPOINT_URL"] = STAGING_SPARQL_BIGDATA_URL
wbi_config["WIKIBASE_URL"] = SVC_URL


def import_entity(username, password, data, label="", item_id=""):
    login_instance = wbi_login.Login(user=username, pwd=password, use_clientlogin=True)

    entity = wbi_core.ItemEngine(data=data, item_id=item_id)
    if label:
        entity.set_label(label, ENGLISH)

    entity_id = entity.write(login_instance)
    return entity_id


def extract_source_entity_codes(catalog_code):
    entity_codes = []

    # Retrieves the entity codes for which we want to download the dataset
    sparql_query = f"""
            SELECT *
            WHERE 
            {{
                ?{SPARQL_A} 
                <{SVC_CATALOG_PROPERTY_URL}>
                <{SVC_ENTITY_URL_PREFIX}{catalog_code}>
            }}"""

    sparql_response = wbi_core.FunctionsEngine.execute_sparql_query(sparql_query)

    for result in sparql_response[RESULTS][BINDINGS]:
        entity_codes.append(
            re.search(SPARQL_ENTITY_CODE_REGEX, result[SPARQL_A][VALUE]).group(1)
        )

    return entity_codes


def extract_dataset_version_codes(entity_code):
    dataset_version_codes = set()

    sparql_query = f"""
            SELECT *
            WHERE 
            {{
                ?{SPARQL_A} 
                <{SVC_SOURCE_PROPERTY_URL}>
                <{SVC_ENTITY_URL_PREFIX}{entity_code}>
            }}"""

    sparql_response = wbi_core.FunctionsEngine.execute_sparql_query(sparql_query)

    for result in sparql_response[RESULTS][BINDINGS]:
        dataset_version_codes.add(
            re.search(SPARQL_ENTITY_CODE_REGEX, result[SPARQL_A][VALUE]).group(1)
        )

    # Verify if entity if part of a catalog of sources.
    # If yes, removes the catalog of sources entity code, which appears in the results of a source entity
    if (
        GTFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes
        or GBFS_CATALOG_OF_SOURCES_CODE in dataset_version_codes
    ):
        dataset_version_codes.discard(GTFS_CATALOG_OF_SOURCES_CODE)
        dataset_version_codes.discard(GBFS_CATALOG_OF_SOURCES_CODE)

    return dataset_version_codes
