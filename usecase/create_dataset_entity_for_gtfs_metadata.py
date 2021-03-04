from wikibaseintegrator import wbi_core
from utilities.request_utils import import_entity
from utilities.constants import (
    STAGING_USERNAME,
    STAGING_PASSWORD,
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


def create_prop_dict(datatype, prop_id, value, rank, if_exists="REPLACE"):
    return {
        DATATYPE: datatype,
        PROP_ID: prop_id,
        VALUE: value,
        RANK: rank,
        IF_EXISTS: if_exists,
    }


def create_dataset_entity_for_gtfs_metadata(gtfs_representation, api_url):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

    label = metadata.dataset_version_name
    instance_prop = create_prop_dict(
        wbi_core.ItemID, INSTANCE_PROP, GTFS_SCHEDULE_DATA_FORMAT, NORMAL
    )
    source_entity_prop = create_prop_dict(
        wbi_core.ItemID, SOURCE_ENTITY_PROP, metadata.source_entity_code, NORMAL
    )
    main_timezone_prop = create_prop_dict(
        wbi_core.String, MAIN_TIMEZONE_PROP, metadata.main_timezone, PREFERRED
    )
    main_language_code_prop = create_prop_dict(
        wbi_core.String, MAIN_LANGUAGE_CODE_PROP, metadata.main_language_code, PREFERRED
    )
    start_service_date_prop = create_prop_dict(
        wbi_core.String, START_SERVICE_DATE_PROP, metadata.start_service_date, NORMAL
    )
    end_service_date_prop = create_prop_dict(
        wbi_core.String, END_SERVICE_DATE_PROP, metadata.end_service_date, NORMAL
    )
    start_timestamp_prop = create_prop_dict(
        wbi_core.String, START_TIMESTAMP_PROP, metadata.start_timestamp, NORMAL
    )
    end_timestamp_prop = create_prop_dict(
        wbi_core.String, END_TIMESTAMP_PROP, metadata.end_timestamp, NORMAL
    )
    md5_hash_prop = create_prop_dict(
        wbi_core.String, MD5_HASH_PROP, metadata.md5_hash, NORMAL
    )

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
        STAGING_USERNAME, STAGING_PASSWORD, dataset_props, label
    )

    version_prop = create_prop_dict(
        wbi_core.ItemID,
        DATASET_VERSION_PROP,
        metadata.dataset_version_entity_code,
        NORMAL,
        if_exists="APPEND",
    )
    source_props = [version_prop]
    import_entity(
        STAGING_USERNAME,
        STAGING_PASSWORD,
        source_props,
        item_id=metadata.source_entity_code,
    )

    return gtfs_representation
