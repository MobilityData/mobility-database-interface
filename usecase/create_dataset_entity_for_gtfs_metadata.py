import os
from wikibaseintegrator import wbi_core
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
    MAIN_LANGUAGE_CODE_PROP,
    START_SERVICE_DATE_PROP,
    END_SERVICE_DATE_PROP,
    START_TIMESTAMP_PROP,
    END_TIMESTAMP_PROP,
    SHA1_HASH_PROP,
    DATASET_VERSION_PROP,
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
)
from utilities.validators import (
    validate_gtfs_representation,
    is_valid_str,
    is_valid_list,
    is_valid_dict,
    is_valid_int,
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


def create_dataset_entity_for_gtfs_metadata(gtfs_representation):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
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
    if is_valid_str(metadata.main_timezone):
        dataset_data.append(
            wbi_core.String(
                value=metadata.main_timezone,
                prop_nr=os.environ[TIMEZONE_PROP],
                rank=PREFERRED,
            )
        )

    # Other timezones property
    if is_valid_list(metadata.other_timezones):
        for timezone in metadata.other_timezones:
            if is_valid_str(timezone):
                dataset_data.append(
                    wbi_core.String(
                        value=timezone, prop_nr=os.environ[TIMEZONE_PROP], rank=NORMAL
                    )
                )

    # Main language code property
    if is_valid_str(metadata.main_language_code):
        dataset_data.append(
            wbi_core.String(
                value=metadata.main_language_code,
                prop_nr=os.environ[MAIN_LANGUAGE_CODE_PROP],
                rank=PREFERRED,
            )
        )

    # Start service date property
    if is_valid_str(metadata.start_service_date):
        dataset_data.append(
            wbi_core.String(
                value=metadata.start_service_date,
                prop_nr=os.environ[START_SERVICE_DATE_PROP],
            )
        )

    # End service date property
    if is_valid_str(metadata.end_service_date):
        dataset_data.append(
            wbi_core.String(
                value=metadata.end_service_date,
                prop_nr=os.environ[END_SERVICE_DATE_PROP],
            )
        )

    # Start timestamp property
    if is_valid_str(metadata.start_timestamp):
        dataset_data.append(
            wbi_core.String(
                value=metadata.start_timestamp, prop_nr=os.environ[START_TIMESTAMP_PROP]
            )
        )

    # End timestamp property
    if is_valid_str(metadata.end_timestamp):
        dataset_data.append(
            wbi_core.String(
                value=metadata.end_timestamp, prop_nr=os.environ[END_TIMESTAMP_PROP]
            )
        )

    # SHA-1 hash property
    if is_valid_str(metadata.sha1_hash):
        dataset_data.append(
            wbi_core.String(
                value=metadata.sha1_hash, prop_nr=os.environ[SHA1_HASH_PROP]
            )
        )

    # Bounding box property
    if is_valid_dict(metadata.bounding_box):
        for order_key, corner_value in metadata.bounding_box.items():
            dataset_data.append(
                create_geographical_property(
                    order_key, corner_value, os.environ[BOUNDING_BOX_PROP]
                )
            )

    # Bounding octagon property
    if is_valid_dict(metadata.bounding_octagon):
        for order_key, corner_value in metadata.bounding_octagon.items():
            dataset_data.append(
                create_geographical_property(
                    order_key, corner_value, os.environ[BOUNDING_OCTAGON_PROP]
                )
            )

    # Stop counts
    if is_valid_dict(metadata.stops_count_by_type):
        # Number of stops property
        if is_valid_int(metadata.stops_count_by_type.get(STOP_KEY)):
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=metadata.stops_count_by_type.get(STOP_KEY),
                    prop_nr=os.environ[NUM_OF_STOPS_PROP],
                )
            )

        # Number of stations property
        if is_valid_int(metadata.stops_count_by_type.get(STATION_KEY)):
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=metadata.stops_count_by_type.get(STATION_KEY),
                    prop_nr=os.environ[NUM_OF_STATIONS_PROP],
                )
            )

        if is_valid_int(metadata.stops_count_by_type.get(ENTRANCE_KEY)):
            # Number of entrances property
            dataset_data.append(
                wbi_core.Quantity(
                    quantity=metadata.stops_count_by_type.get(ENTRANCE_KEY),
                    prop_nr=os.environ[NUM_OF_ENTRANCES_PROP],
                )
            )

    if is_valid_int(metadata.agencies_count):
        # Number of agencies property
        dataset_data.append(
            wbi_core.Quantity(
                quantity=metadata.agencies_count,
                prop_nr=os.environ[NUM_OF_AGENCIES_PROP],
            )
        )

    # Number of routes property
    if is_valid_dict(metadata.routes_count_by_type):
        for route_key, route_value in metadata.routes_count_by_type.items():
            if is_valid_int(route_value):
                route_qualifier = [
                    wbi_core.String(
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

    metadata.dataset_version_entity_code = import_entity(
        os.environ[USERNAME], os.environ[PASSWORD], dataset_data, version_name_label
    )

    version_prop = wbi_core.ItemID(
        value=metadata.dataset_version_entity_code,
        prop_nr=os.environ[DATASET_VERSION_PROP],
        if_exists=APPEND,
    )
    source_data = [version_prop]
    metadata.source_entity_code = import_entity(
        os.environ[USERNAME],
        os.environ[PASSWORD],
        source_data,
        item_id=metadata.source_entity_code,
    )

    return gtfs_representation
