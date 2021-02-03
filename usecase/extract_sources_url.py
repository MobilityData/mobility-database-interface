import requests
from request_manager.sparql_request_helper import sparql_request
from utilities.constants import (
    GTFS_CATALOG_OF_SOURCES, GBFS_CATALOG_OF_SOURCES,
    DATASET_VERSION_ENTITY_CODE_FIRST_INDEX,
    DATASET_VERSION_ENTITY_CODE_LAST_INDEX,
    ACTION, IDS, LANGUAGES, FORMAT,
    ENTITIES, CLAIMS, MAINSNAK, DATAVALUE, VALUE,
    WB_GET_ENTITIES, RESULTS, BINDINGS
)
from utilities.validators import validate_urls


def extract_source_url(api_url, sparql_api, dataset_type="GTFS", specific_download=False,
                 specific_entity_code=None):
    """Extracts a list of urls of a given dataset
    :param api_url: either STAGING_API_URL or PRODUCTION_API_URL in utilities/constants.py
    :param sparql_api: either STAGING_SPARQL_URL or PRODUCTION_SPARQL_URL in utilities/constants.py
    :param dataset_type: Dataset type, GTFS or GBFS. Default to GTFS.
    :param specific_download: True if the URL must be extracted for a specific dataset, false otherwise.
    :param specific_entity_code: Entity code of the specific dataset for which the URL must be extracted.
    Required if `specific_download` is set to True.
    :return: URLs of the datasets in the database, for the `dataset_type` passed in the constructor.
    """

    validate_urls(api_url, sparql_api)
    if dataset_type == "GTFS":
        catalog_code = GTFS_CATALOG_OF_SOURCES
    elif dataset_type == "GBFS":
        catalog_code = GBFS_CATALOG_OF_SOURCES
    else:
        raise NotImplementedError()

    entity_codes = []
    urls = {}

    # Retrieves the entity codes for which we want to download the dataset
    if not specific_download:

        sparql_response = sparql_request(sparql_api,
            f"""
            SELECT *
            WHERE 
            {{
                ?a 
                <http://wikibase.svc/prop/statement/P65>
                <http://wikibase.svc/entity/{catalog_code}>
            }}"""  # double curly bracket escapes a curly bracket
        )

        for result in sparql_response[RESULTS][BINDINGS]:
            entity_codes.append(
                result['a'][VALUE][DATASET_VERSION_ENTITY_CODE_FIRST_INDEX:DATASET_VERSION_ENTITY_CODE_LAST_INDEX]
            )
    else:
        entity_codes.append(specific_entity_code)

    # Retrieves the sources' stable URL for the entity codes found
    for entity_code in entity_codes:
        params = {
            ACTION: WB_GET_ENTITIES,
            IDS: f"{entity_code}",
            LANGUAGES: "en",
            FORMAT: "json"
        }
        api_response = requests.get(api_url, params)
        api_response.raise_for_status()
        json_response = api_response.json()

        if ENTITIES not in json_response:
            continue
        for link in json_response[ENTITIES][entity_code][CLAIMS]["P55"]:
            if "openmobilitydata.org" not in link[MAINSNAK][DATAVALUE][VALUE]:
                urls[entity_code] = link[MAINSNAK][DATAVALUE][VALUE]

    return urls
