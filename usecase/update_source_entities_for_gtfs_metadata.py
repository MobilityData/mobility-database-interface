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
from utilities.validators import validate_datasets_infos, validate_api_url


def create_data(version_code):
    return f"""{{
            "claims": {{
                "P64":[
                    {{
                        "mainsnak":{{
                            "snaktype":"value",
                            "property":"P64",
                            "datavalue":{{
                                "value":{{
                                    "entity-type":"item",
                                    "id":"{version_code}"
                                }},
                                "type":"wikibase-entityid"
                            }},
                            "datatype":"wikibase-item"
                        }},
                        "type":"statement",
                        "rank":"normal"
                    }}
                ]
            }}
        }}"""


def update_source_entities_for_gtfs_metadata(datasets_infos, api_url, sparql_api):
    """Update the source entities with their new dataset versions.
    :param datasets_infos: A list of dataset infos, for the datasets to load.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :param sparql_api: SPARQL api, either PRODUCTION_SPARQL_URL or STAGING_SPARQL_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_datasets_infos(datasets_infos)

    for dataset_infos in datasets_infos:
        dataset_version_codes = set()

        sparql_response = sparql_request(
            sparql_api,
            f"""
                    SELECT *
                    WHERE 
                    {{
                        ?a 
                        <http://wikibase.svc/prop/statement/P48>
                        <http://wikibase.svc/entity/{dataset_infos.entity_code}>
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

        # Remove the previous versions from the dataset version codes set
        dataset_version_codes = dataset_version_codes.difference(
            dataset_infos.previous_versions
        )

        # Step 1: GET request to fetch login token
        PARAMS_LOGIN_TOKEN = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json",
        }

        api_response = requests.get(api_url, params=PARAMS_LOGIN_TOKEN)
        api_response.raise_for_status()
        response_data = api_response.json()

        LOGIN_TOKEN = response_data["query"]["tokens"]["logintoken"]

        # Step 2: POST request to log in. Use of main account for login is not
        # supported. Obtain credentials via Special:BotPasswords
        # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
        PARAMS_LOGIN = {
            "action": "login",
            "lgname": "MaximeArmstrong",
            "lgpassword": "j9-sb4E7AKFTu8iVp93erLuYqqNeKv3ZyvN7cNKG",
            "lgtoken": LOGIN_TOKEN,
            "format": "json",
        }

        api_response = requests.post(api_url, data=PARAMS_LOGIN_TOKEN)
        api_response.raise_for_status()
        # response = api_response.json()

        # Step 3: GET request to fetch CSRF token
        PARAMS_CSRF_TOKEN = {"action": "query", "meta": "tokens", "format": "json"}

        api_response = requests.get(api_url, params=PARAMS_CSRF_TOKEN)
        api_response.raise_for_status()
        response_data = api_response.json()

        CSRF_TOKEN = response_data["query"]["tokens"]["csrftoken"]

        for version_code in dataset_version_codes:
            # Step 4: POST request to edit a page
            PARAMS_ENTITY_CREATION = {
                "action": "wbeditentity",
                "id": f"{dataset_infos.entity_code}",
                "data": f"{create_data(version_code)}",
                "token": CSRF_TOKEN,
            }

            api_response = requests.post(api_url, data=PARAMS_ENTITY_CREATION)
            api_response.raise_for_status()
