import requests
import re

from request_manager.sparql_request_helper import sparql_request
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES_CODE,
    GBFS_CATALOG_OF_SOURCES_CODE,
    RESULTS,
    BINDINGS,
    VALUE,
    SPARQL_ENTITY_CODE_REGEX,
    ID,
    ENTITY_TYPE,
    ITEM,
    WIKIBASE_ENTITYID,
    WIKIBASE_ITEM,
    STRING,
    MAINSNAK,
    TYPE,
    DATATYPE,
    DATAVALUE,
    RANK,
    STATEMENT,
    SNAKTYPE,
    PROPERTY,
    ACTION,
    META,
    FORMAT,
    JSON,
    LOGIN,
    TOKENS,
    QUERY,
    LOGIN_TOKEN,
    CSRF_TOKEN,
    LGTOKEN,
    LGPASSWORD,
    LGNAME,
    STAGING_USERNAME,
    STAGING_PASSWORD,
    SPARQL_A,
    SVC_SOURCE_PROPERTY_URL,
    SVC_ENTITY_URL_PREFIX,
)


def create_wikibase_item_claim_string(property_id, entity_id, rank):
    value = f"""{{
                "{ENTITY_TYPE}":"{ITEM}", 
                "{ID}":"{entity_id}"
            }}"""
    return create_claim_string(
        property_id, value, rank, WIKIBASE_ENTITYID, WIKIBASE_ITEM
    )


def create_regular_claim_string(property_id, value, rank):
    value = f'"{value}"'
    return create_claim_string(property_id, value, rank, STRING, STRING)


def create_claim_string(property_id, value, rank, type, datatype):
    return f"""
        "{property_id}":[
            {{
                "{MAINSNAK}": {{
                    "{SNAKTYPE}": "{VALUE}",
                    "{PROPERTY}": "{property_id}",
                    "{DATAVALUE}": {{
                        "{VALUE}": {value},
                        "{TYPE}": "{type}"
                    }},
                    "{DATATYPE}": "{datatype}"
                }},
                "{TYPE}": "{STATEMENT}",
                "{RANK}": "{rank}"
            }}
        ]
        """


def create_geographical_claim_string(property_id, value, rank):
    raise NotImplementedError


def create_geographical_item(rank, value):
    raise NotImplementedError


def extract_dataset_version_codes(entity_code, sparql_api):
    dataset_version_codes = set()

    sparql_response = sparql_request(
        sparql_api,
        f"""
            SELECT *
            WHERE 
            {{
                ?{SPARQL_A} 
                <{SVC_SOURCE_PROPERTY_URL}>
                <{SVC_ENTITY_URL_PREFIX}{entity_code}>
            }}""",
    )

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


def generate_api_csrf_token(api_url):
    # Get login token
    params_login_token = {
        ACTION: QUERY,
        META: TOKENS,
        TYPE: LOGIN,
        FORMAT: JSON,
    }
    api_response = requests.get(api_url, params=params_login_token)
    api_response.raise_for_status()
    response_data = api_response.json()
    login_token = response_data[QUERY][TOKENS][LOGIN_TOKEN]

    # Login to database
    params_login = {
        ACTION: LOGIN,
        LGNAME: STAGING_USERNAME,
        LGPASSWORD: STAGING_PASSWORD,
        LGTOKEN: login_token,
        FORMAT: JSON,
    }
    api_response = requests.post(api_url, data=params_login)
    api_response.raise_for_status()

    # Get csrf token
    params_csrf_token = {ACTION: QUERY, META: TOKENS, FORMAT: JSON}
    api_response = requests.get(api_url, params=params_csrf_token)
    api_response.raise_for_status()
    response_data = api_response.json()
    csrf_token = response_data[QUERY][TOKENS][CSRF_TOKEN]

    return csrf_token
