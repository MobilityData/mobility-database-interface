import requests


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


def generate_api_csrf_token(api_url):
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

    api_response = requests.post(api_url, data=PARAMS_LOGIN)
    api_response.raise_for_status()

    # Step 3: GET request to fetch CSRF token
    PARAMS_CSRF_TOKEN = {"action": "query", "meta": "tokens", "format": "json"}

    api_response = requests.get(api_url, params=PARAMS_CSRF_TOKEN)
    api_response.raise_for_status()
    response_data = api_response.json()

    CSRF_TOKEN = response_data["query"]["tokens"]["csrftoken"]
    return CSRF_TOKEN
