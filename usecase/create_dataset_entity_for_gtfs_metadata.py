import os
from dotenv import load_dotenv

from wikibaseintegrator import wbi_core
from utilities.request_utils import import_entity
from utilities.constants import (
    DATATYPE,
    PROP_ID,
    VALUE,
    RANK,
    IF_EXISTS,
    NORMAL,
    PREFERRED,
    INSTANCE_PROP,
    SOURCE_ENTITY_PROP,
    MAIN_TIMEZONE_PROP,
    MAIN_LANGUAGE_CODE_PROP,
    START_SERVICE_DATE_PROP,
    END_SERVICE_DATE_PROP,
    START_TIMESTAMP_PROP,
    END_TIMESTAMP_PROP,
    MD5_HASH_PROP,
    DATASET_VERSION_PROP,
    GTFS_SCHEDULE_DATA_FORMAT,
)
from utilities.validators import validate_gtfs_representation, validate_api_url

load_dotenv()
STAGING_USERNAME = os.getenv("STAGING_USERNAME")
STAGING_PASSWORD = os.getenv("STAGING_PASSWORD")

REPLACE = "REPLACE"
APPEND = "APPEND"


def create_dataset_entity_for_gtfs_metadata(gtfs_representation, api_url):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

    version_name_label = metadata.dataset_version_name
    instance_prop = {
        DATATYPE: wbi_core.ItemID,
        PROP_ID: INSTANCE_PROP,
        VALUE: GTFS_SCHEDULE_DATA_FORMAT,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    source_entity_prop = {
        DATATYPE: wbi_core.ItemID,
        PROP_ID: SOURCE_ENTITY_PROP,
        VALUE: metadata.source_entity_code,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    main_timezone_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: MAIN_TIMEZONE_PROP,
        VALUE: metadata.main_timezone,
        RANK: PREFERRED,
        IF_EXISTS: REPLACE,
    }
    main_language_code_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: MAIN_LANGUAGE_CODE_PROP,
        VALUE: metadata.main_language_code,
        RANK: PREFERRED,
        IF_EXISTS: REPLACE,
    }
    start_service_date_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: START_SERVICE_DATE_PROP,
        VALUE: metadata.start_service_date,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    end_service_date_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: END_SERVICE_DATE_PROP,
        VALUE: metadata.end_service_date,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    start_timestamp_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: START_TIMESTAMP_PROP,
        VALUE: metadata.start_timestamp,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    end_timestamp_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: END_TIMESTAMP_PROP,
        VALUE: metadata.end_timestamp,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }
    md5_hash_prop = {
        DATATYPE: wbi_core.String,
        PROP_ID: MD5_HASH_PROP,
        VALUE: metadata.md5_hash,
        RANK: NORMAL,
        IF_EXISTS: REPLACE,
    }

    dataset_props = [
        instance_prop,
        source_entity_prop,
        main_timezone_prop,
        main_language_code_prop,
        start_service_date_prop,
        end_service_date_prop,
        start_timestamp_prop,
        end_timestamp_prop,
        md5_hash_prop,
    ]
    metadata.dataset_version_entity_code = import_entity(
        STAGING_USERNAME, STAGING_PASSWORD, dataset_props, version_name_label
    )

    version_prop = {
        DATATYPE: wbi_core.ItemID,
        PROP_ID: DATASET_VERSION_PROP,
        VALUE: metadata.dataset_version_entity_code,
        RANK: NORMAL,
        IF_EXISTS: APPEND,
    }
    source_props = [version_prop]
    metadata.source_entity_code = import_entity(
        STAGING_USERNAME,
        STAGING_PASSWORD,
        source_props,
        item_id=metadata.source_entity_code,
    )

    return gtfs_representation
