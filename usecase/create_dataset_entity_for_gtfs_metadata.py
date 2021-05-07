import os
from wikibaseintegrator import wbi_core, wbi_login
from utilities.request_utils import import_entity
from utilities.constants import (
    NORMAL,
    PREFERRED,
    LAT,
    LON,
    GLOBE_PRECISION,
    GLOBE_URL,
    STOP_KEY,
    STATION_KEY,
    ENTRANCE_KEY,
    APPEND,
    GTFS_SCHEDULE_DATA_FORMAT,
    INSTANCE_PROP,
    SOURCE_ENTITY_PROP,
    TIMEZONE_PROP,
    COUNTRY_CODE_PROP,
    MAIN_LANGUAGE_CODE_PROP,
    START_SERVICE_DATE_PROP,
    END_SERVICE_DATE_PROP,
    START_TIMESTAMP_PROP,
    END_TIMESTAMP_PROP,
    SHA1_HASH_PROP,
    DATASET_PROP,
    ORDER_PROP,
    BOUNDING_BOX_PROP,
    BOUNDING_OCTAGON_PROP,
    NUM_OF_STOPS_PROP,
    NUM_OF_STATIONS_PROP,
    NUM_OF_ENTRANCES_PROP,
    NUM_OF_AGENCIES_PROP,
    NUM_OF_ROUTES_PROP,
    ROUTE_TYPE_PROP,
    USERNAME,
    PASSWORD,
    ENGLISH,
    DOWNLOAD_DATE_PROP,
)
from utilities.validators import (
    validate_gtfs_representation,
    is_valid_instance,
    validate_api_url,
)


def create_geographical_property(order_key, corner_value, property_type):
    order_qualifier = [
        wbi_core.Quantity(
            quantity=order_key, prop_nr=os.environ[ORDER_PROP], is_qualifier=True
        )
    ]

    return wbi_core.GlobeCoordinate(
        latitude=corner_value.get(LAT),
        longitude=corner_value.get(LON),
        precision=GLOBE_PRECISION,
        globe=GLOBE_URL,
        prop_nr=property_type,
        qualifiers=order_qualifier,
    )


def create_dataset_entity_for_gtfs_metadata(
    gtfs_representation, api_url, username=None, password=None
):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

    dataset_data = []

    # Instance property
    dataset_data.append(
        wbi_core.ItemID(
            value=os.environ[GTFS_SCHEDULE_DATA_FORMAT],
            prop_nr=os.environ[INSTANCE_PROP],
        )
    )

    # Source entity property
    dataset_data.append(
        wbi_core.ItemID(
            value=metadata.source_entity_code, prop_nr=os.environ[SOURCE_ENTITY_PROP]
        )
    )

    # Main timezone property
    if is_valid_instance(metadata.main_timezone, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.main_timezone,
                prop_nr=os.environ[TIMEZONE_PROP],
                rank=PREFERRED,
            )
        )

    # Other timezones property
    if is_valid_instance(metadata.other_timezones, list):
        for timezone in metadata.other_timezones:
            dataset_data.append(
                wbi_core.String(
                    value=timezone, prop_nr=os.environ[TIMEZONE_PROP], rank=NORMAL
                )
            )

    # Country code property
    if is_valid_instance(metadata.country_codes, list):
        for country_code in metadata.country_codes:
            dataset_data.append(
                wbi_core.String(
                    value=country_code,
                    prop_nr=os.environ[COUNTRY_CODE_PROP],
                    rank=NORMAL,
                )
            )

    # Main language code property
    if is_valid_instance(metadata.main_language_code, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.main_language_code,
                prop_nr=os.environ[MAIN_LANGUAGE_CODE_PROP],
                rank=PREFERRED,
            )
        )

    # Start service date property
    if is_valid_instance(metadata.start_service_date, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.start_service_date,
                prop_nr=os.environ[START_SERVICE_DATE_PROP],
            )
        )

    # End service date property
    if is_valid_instance(metadata.end_service_date, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.end_service_date,
                prop_nr=os.environ[END_SERVICE_DATE_PROP],
            )
        )

    # Start timestamp property
    if is_valid_instance(metadata.start_timestamp, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.start_timestamp, prop_nr=os.environ[START_TIMESTAMP_PROP]
            )
        )

    # End timestamp property
    if is_valid_instance(metadata.end_timestamp, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.end_timestamp, prop_nr=os.environ[END_TIMESTAMP_PROP]
            )
        )

    # SHA-1 hash property
    if is_valid_instance(metadata.sha1_hash, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.sha1_hash, prop_nr=os.environ[SHA1_HASH_PROP]
            )
        )

    # Bounding box property
    if is_valid_instance(metadata.bounding_box, dict):
        for order_key, corner_value in metadata.bounding_box.items():
            dataset_data.append(
                create_geographical_property(
                    order_key, corner_value, os.environ[BOUNDING_BOX_PROP]
                )
            )

    # Bounding octagon property
    if is_valid_instance(metadata.bounding_octagon, dict):
        for order_key, corner_value in metadata.bounding_octagon.items():
            dataset_data.append(
                create_geographical_property(
                    order_key, corner_value, os.environ[BOUNDING_OCTAGON_PROP]
                )
            )

    # Stop counts
    if is_valid_instance(metadata.stops_count_by_type, dict):
        # Number of stops property
        stops_count = metadata.stops_count_by_type.get(STOP_KEY, None)
        if stops_count is not None:
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=stops_count,
                    prop_nr=os.environ[NUM_OF_STOPS_PROP],
                )
            )

        # Number of stations property
        stations_count = metadata.stops_count_by_type.get(STATION_KEY, None)
        if stations_count is not None:
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=stations_count,
                    prop_nr=os.environ[NUM_OF_STATIONS_PROP],
                )
            )

        # Number of entrances property
        entrances_count = metadata.stops_count_by_type.get(ENTRANCE_KEY, None)
        if entrances_count is not None:
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=entrances_count,
                    prop_nr=os.environ[NUM_OF_ENTRANCES_PROP],
                )
            )

    if is_valid_instance(metadata.agencies_count, int):
        # Number of agencies property
        dataset_data.append(
            wbi_core.Quantity(
                quantity=metadata.agencies_count,
                prop_nr=os.environ[NUM_OF_AGENCIES_PROP],
            )
        )

    if is_valid_instance(metadata.download_date, str):
        dataset_data.append(
            wbi_core.String(
                value=metadata.download_date,
                prop_nr=os.environ[DOWNLOAD_DATE_PROP],
            )
        )

    # Number of routes property
    if is_valid_instance(metadata.routes_count_by_type, dict):
        for route_key, route_value in metadata.routes_count_by_type.items():
            route_qualifier = [
                wbi_core.ItemID(
                    value=route_key,
                    prop_nr=os.environ[ROUTE_TYPE_PROP],
                    is_qualifier=True,
                )
            ]
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=route_value,
                    prop_nr=os.environ[NUM_OF_ROUTES_PROP],
                    qualifiers=route_qualifier,
                )
            )

    # Dataset version entity label
    version_name_label = metadata.dataset_version_name
    if not username:
        username = os.environ[USERNAME]
    if not password:
        password = os.environ[PASSWORD]
    login_instance = wbi_login.Login(user=username, pwd=password, use_clientlogin=True)
    dataset_entity = wbi_core.ItemEngine(
        data=dataset_data,
        core_props={os.environ[SHA1_HASH_PROP], os.environ[DOWNLOAD_DATE_PROP]},
    )
    dataset_entity.set_label(version_name_label, ENGLISH)
    dataset_entity_id = dataset_entity.write(login_instance)
    metadata.dataset_version_entity_code = dataset_entity_id

    version_prop = wbi_core.ItemID(
        value=metadata.dataset_version_entity_code,
        prop_nr=os.environ[DATASET_PROP],
        if_exists=APPEND,
    )
    source_data = [version_prop]
    source_entity = wbi_core.ItemEngine(item_id=metadata.source_entity_code)
    source_entity.update(source_data)
    source_entity.write(login_instance)
    metadata.source_entity_code = source_entity.item_id

    return gtfs_representation
