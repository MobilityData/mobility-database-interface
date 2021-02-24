from utilities.validators import validate_gtfs_representation, validate_api_url
import requests


def create_data(metadata):
    return f"""{{
            "labels": {{
                "en": {{
                    "language": "en",
                    "value": "{metadata.dataset_version_name}"
                }}
            }},
            "claims": {{
                "P20": [
                    {{
                        "mainsnak": {{
                            "snaktype": "value",
                            "property": "P20",
                            "datavalue": {{
                                "value": {{
                                    "entity-type": "item",
                                    "numeric-id": 29,
                                    "id": "Q29"
                                }},
                                "type": "wikibase-entityid"
                            }},
                            "datatype": "wikibase-item"
                        }},
                        "type": "statement",
                        "rank": "normal"
                    }}
                ],
                {create_regular_claim_string("P49", metadata.main_timezone, "preferred")},
                {create_regular_claim_string("P54", metadata.main_language_code, "preferred")},
                {create_regular_claim_string("P52", metadata.start_service_date, "normal")},
                {create_regular_claim_string("P53", metadata.end_service_date, "normal")},
                {create_regular_claim_string("P66", metadata.start_timestamp, "normal")},
                {create_regular_claim_string("P67", metadata.end_timestamp, "normal")},
                {create_regular_claim_string("P61", metadata.md5_hash, "normal")}
            }}
        }}"""


def create_regular_claim_string(property_id, value, rank):
    return f"""
        "{property_id}":[
            {{
                "mainsnak": {{
                    "snaktype": "value",
                    "property": "{property_id}",
                    "datavalue": {{
                        "value": "{value}",
                        "type": "string"
                    }},
                    "datatype": "string"
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


def create_dataset_entity_for_gtfs_metadata(gtfs_representation, api_url):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

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

    # Step 4: POST request to edit a page
    PARAMS_ENTITY_CREATION = {
        "action": "wbeditentity",
        "new": "item",
        "data": f"{create_data(metadata)}",
        "token": CSRF_TOKEN,
    }

    api_response = requests.post(api_url, data=PARAMS_ENTITY_CREATION)
    api_response.raise_for_status()
    # response = api_response.json()

    return gtfs_representation
