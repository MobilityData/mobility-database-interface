import re
import os

from utilities.constants import (
    RESULTS,
    BINDINGS,
    VALUE,
    SPARQL_ENTITY_CODE_REGEX,
    ENGLISH,
    SPARQL_A,
    SVC_ENTITY_URL_PATH,
    SVC_PROP_URL_PATH,
    SVC_URL,
)

from wikibaseintegrator import wbi_core, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config


def import_entity(username, password, data, label="", item_id=""):
    # Get environment variables
    sparql_bigdata_url = os.environ.get("SPARQL_BIGDATA_URL")
    api_url = os.environ.get("API_URL")

    wbi_config["MEDIAWIKI_API_URL"] = api_url
    wbi_config["SPARQL_ENDPOINT_URL"] = sparql_bigdata_url
    wbi_config["WIKIBASE_URL"] = SVC_URL

    login_instance = wbi_login.Login(user=username, pwd=password, use_clientlogin=True)

    entity = wbi_core.ItemEngine(data=data, item_id=item_id)
    if label:
        entity.set_label(label, ENGLISH)

    entity_id = entity.write(login_instance)
    return entity_id


def extract_source_entity_codes(catalog_code):
    # Get environment variables
    catalog_prop = os.environ.get("CATALOG_PROP")

    entity_codes = []

    # Retrieves the entity codes for which we want to download the dataset
    sparql_query = f"""
            SELECT *
            WHERE 
            {{
                ?{SPARQL_A} 
                <{SVC_URL}{SVC_PROP_URL_PATH}{catalog_prop}>
                <{SVC_URL}{SVC_ENTITY_URL_PATH}{catalog_code}>
            }}"""

    sparql_response = wbi_core.FunctionsEngine.execute_sparql_query(sparql_query)

    for result in sparql_response[RESULTS][BINDINGS]:
        entity_codes.append(
            re.search(SPARQL_ENTITY_CODE_REGEX, result[SPARQL_A][VALUE]).group(1)
        )

    return entity_codes


def extract_dataset_version_codes(entity_code):
    # Get environment variables
    gtfs_catalog_of_sources_code = os.environ.get("GTFS_CATALOG_OF_SOURCES_CODE")
    gbfs_catalog_of_sources_code = os.environ.get("GBFS_CATALOG_OF_SOURCES_CODE")
    source_entity_prop = os.environ.get("SOURCE_ENTITY_PROP")

    dataset_version_codes = set()

    sparql_query = f"""
            SELECT *
            WHERE 
            {{
                ?{SPARQL_A} 
                <{SVC_URL}{SVC_PROP_URL_PATH}{source_entity_prop}>
                <{SVC_URL}{SVC_ENTITY_URL_PATH}{entity_code}>
            }}"""

    sparql_response = wbi_core.FunctionsEngine.execute_sparql_query(sparql_query)

    for result in sparql_response[RESULTS][BINDINGS]:
        dataset_version_codes.add(
            re.search(SPARQL_ENTITY_CODE_REGEX, result[SPARQL_A][VALUE]).group(1)
        )

    # Verify if entity if part of a catalog of sources.
    # If yes, removes the catalog of sources entity code, which appears in the results of a source entity
    if (
        gtfs_catalog_of_sources_code in dataset_version_codes
        or gbfs_catalog_of_sources_code in dataset_version_codes
    ):
        dataset_version_codes.discard(gtfs_catalog_of_sources_code)
        dataset_version_codes.discard(gbfs_catalog_of_sources_code)

    return dataset_version_codes
