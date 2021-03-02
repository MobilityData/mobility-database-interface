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
)


def create_wikibase_item_claim_string(property_id, entity_id, rank):
    value = f"""{{
                "entity-type":"item", 
                "id":"{entity_id}"
            }}"""
    return create_claim_string(
        property_id, value, rank, "wikibase-entityid", "wikibase-item"
    )


def create_regular_claim_string(property_id, value, rank):
    value = f'"{value}"'
    return create_claim_string(property_id, value, rank, "string", "string")


def create_claim_string(property_id, value, rank, type, datatype):
    return f"""
        "{property_id}":[
            {{
                "mainsnak": {{
                    "snaktype": "value",
                    "property": "{property_id}",
                    "datavalue": {{
                        "value": {value},
                        "type": "{type}"
                    }},
                    "datatype": "{datatype}"
                }},
                "type": "statement",
                "rank": "{rank}"
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
                ?a 
                <http://wikibase.svc/prop/statement/P48>
                <http://wikibase.svc/entity/{entity_code}>
            }}""",
    )

    for result in sparql_response[RESULTS][BINDINGS]:
        dataset_version_codes.add(
            re.search(SPARQL_ENTITY_CODE_REGEX, result["a"][VALUE]).group(1)
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
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json",
    }
    api_response = requests.get(api_url, params=params_login_token)
    api_response.raise_for_status()
    response_data = api_response.json()
    login_token = response_data["query"]["tokens"]["logintoken"]

    # Login to database
    params_login = {
        "action": "login",
        "lgname": "MaximeArmstrong",
        "lgpassword": "j9-sb4E7AKFTu8iVp93erLuYqqNeKv3ZyvN7cNKG",
        "lgtoken": login_token,
        "format": "json",
    }
    api_response = requests.post(api_url, data=params_login)
    api_response.raise_for_status()

    # Get csrf token
    params_csrf_token = {"action": "query", "meta": "tokens", "format": "json"}
    api_response = requests.get(api_url, params=params_csrf_token)
    api_response.raise_for_status()
    response_data = api_response.json()
    csrf_token = response_data["query"]["tokens"]["csrftoken"]

    return csrf_token
