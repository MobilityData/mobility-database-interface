import requests
from utilities.request_utils import (
    create_wikibase_item_claim_string,
    create_regular_claim_string,
    generate_api_csrf_token,
)
from utilities.constants import (
    ACTION,
    WB_EDIT_ENTITY,
    NEW,
    ITEM,
    DATA,
    TOKEN,
)
from utilities.validators import validate_gtfs_representation, validate_api_url


def create_data(metadata):
    return f"""{{
            "labels": {{
                "en": {{
                    "language": "en",
                    "value": "{metadata.dataset_version_name}"
                }}
            }},
            "claims": {{
                {create_wikibase_item_claim_string("P20", "Q29", "normal")},
                {create_wikibase_item_claim_string("P48", metadata.source_entity_code, "normal")},
                {create_regular_claim_string("P49", metadata.main_timezone, "preferred")},
                {create_regular_claim_string("P54", metadata.main_language_code, "preferred")},
                {create_regular_claim_string("P52", metadata.start_service_date, "normal")},
                {create_regular_claim_string("P53", metadata.end_service_date, "normal")},
                {create_regular_claim_string("P66", metadata.start_timestamp, "normal")},
                {create_regular_claim_string("P67", metadata.end_timestamp, "normal")},
                {create_regular_claim_string("P61", metadata.md5_hash, "normal")}
            }}
        }}"""


def create_dataset_entity_for_gtfs_metadata(gtfs_representation, api_url):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

    csrf_token = generate_api_csrf_token(api_url)

    # Step 4: POST request to edit a page
    params_entity_creation = {
        ACTION: WB_EDIT_ENTITY,
        NEW: ITEM,
        DATA: f"{create_data(metadata)}",
        TOKEN: csrf_token,
    }

    api_response = requests.post(api_url, data=params_entity_creation)
    api_response.raise_for_status()

    return gtfs_representation
