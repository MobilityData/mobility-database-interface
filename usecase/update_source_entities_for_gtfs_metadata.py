import requests

from utilities.constants import (
    ACTION,
    ID,
    WB_EDIT_ENTITY,
    DATA,
    TOKEN,
)
from utilities.request_utils import (
    create_wikibase_item_claim_string,
    extract_dataset_version_codes,
    generate_api_csrf_token,
)
from utilities.validators import (
    validate_datasets_infos,
    validate_api_url,
    validate_sparql_url,
)


def create_data(version_code):
    return f"""{{
            "claims":{{
                {create_wikibase_item_claim_string("P64", version_code, "normal")}
            }}
        }}"""


def update_source_entities_for_gtfs_metadata(datasets_infos, api_url, sparql_api):
    """Update the source entities with their new dataset versions.
    :param datasets_infos: A list of dataset infos, for the datasets to load.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :param sparql_api: SPARQL api, either PRODUCTION_SPARQL_URL or STAGING_SPARQL_URL.
    :return: The datasets infos post-execution.
    """
    validate_api_url(api_url)
    validate_sparql_url(sparql_api)
    validate_datasets_infos(datasets_infos)

    for dataset_infos in datasets_infos:
        dataset_version_codes = extract_dataset_version_codes(
            dataset_infos.entity_code, sparql_api
        )

        # Remove the previous versions from the dataset version codes set
        dataset_version_codes = dataset_version_codes.difference(
            dataset_infos.previous_versions
        )

        csrf_token = generate_api_csrf_token(api_url)

        for version_code in dataset_version_codes:
            # Step 4: POST request to edit a page
            params_entity_creation = {
                ACTION: WB_EDIT_ENTITY,
                ID: f"{dataset_infos.entity_code}",
                DATA: f"{create_data(version_code)}",
                TOKEN: csrf_token,
            }

            api_response = requests.post(api_url, data=params_entity_creation)
            api_response.raise_for_status()

    return datasets_infos
