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
)
from utilities.validators import validate_gtfs_representation, validate_api_url


def create_geographical_property(order_key, corner_value, property_type):
    # Get environment variables
    order_prop = os.environ.get("ORDER_PROP")

    order_qualifier = [
        wbi_core.Quantity(quantity=order_key, prop_nr=order_prop, is_qualifier=True)
    ]

    return wbi_core.GlobeCoordinate(
        latitude=corner_value.get(LAT),
        longitude=corner_value.get(LON),
        precision=GLOBE_PRECISION,
        globe=GLOBE_URL,
        prop_nr=property_type,
        qualifiers=order_qualifier,
    )


def create_dataset_entity_for_gtfs_metadata(gtfs_representation, api_url):
    """Create a dataset entity for a new dataset version on the Database.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :param api_url: API url, either PRODUCTION_API_URL or STAGING_API_URL.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_api_url(api_url)
    validate_gtfs_representation(gtfs_representation)
    metadata = gtfs_representation.metadata

    # Get environment variables
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    gtfs_schedule_data_format = os.environ.get("GTFS_SCHEDULE_DATA_FORMAT")
    instance_prop = os.environ.get("INSTANCE_PROP")
    source_entity_prop = os.environ.get("SOURCE_ENTITY_PROP")
    timezone_prop = os.environ.get("TIMEZONE_PROP")
    main_language_code_prop = os.environ.get("MAIN_LANGUAGE_CODE_PROP")
    start_service_date_prop = os.environ.get("START_SERVICE_DATE_PROP")
    end_service_date_prop = os.environ.get("END_SERVICE_DATE_PROP")
    start_timestamp_prop = os.environ.get("START_TIMESTAMP_PROP")
    end_timestamp_prop = os.environ.get("END_TIMESTAMP_PROP")
    md5_hash_prop = os.environ.get("MD5_HASH_PROP")
    dataset_version_prop = os.environ.get("DATASET_VERSION_PROP")
    bounding_box_prop = os.environ.get("BOUNDING_BOX_PROP")
    bounding_octagon_prop = os.environ.get("BOUNDING_OCTAGON_PROP")
    num_of_stops_prop = os.environ.get("NUM_OF_STOPS_PROP")
    num_of_stations_prop = os.environ.get("NUM_OF_STATIONS_PROP")
    num_of_entrances_prop = os.environ.get("NUM_OF_ENTRANCES_PROP")
    num_of_agencies_prop = os.environ.get("NUM_OF_AGENCIES_PROP")
    num_of_routes_prop = os.environ.get("NUM_OF_ROUTES_PROP")
    route_type_prop = os.environ.get("ROUTE_TYPE_PROP")

    dataset_data = []

    # Instance property
    dataset_data.append(
        wbi_core.ItemID(value=gtfs_schedule_data_format, prop_nr=instance_prop)
    )

    # Source entity property
    dataset_data.append(
        wbi_core.ItemID(value=metadata.source_entity_code, prop_nr=source_entity_prop)
    )

    # Main timezone property
    dataset_data.append(
        wbi_core.String(
            value=metadata.main_timezone, prop_nr=timezone_prop, rank=PREFERRED
        )
    )

    # Other timezones property
    for timezone in metadata.other_timezones:
        dataset_data.append(
            wbi_core.String(value=timezone, prop_nr=timezone_prop, rank=NORMAL)
        )

    # Main language code property
    dataset_data.append(
        wbi_core.String(
            value=metadata.main_language_code,
            prop_nr=main_language_code_prop,
            rank=PREFERRED,
        )
    )

    # Start service date property
    dataset_data.append(
        wbi_core.String(
            value=metadata.start_service_date, prop_nr=start_service_date_prop
        )
    )

    # End service date property
    dataset_data.append(
        wbi_core.String(value=metadata.end_service_date, prop_nr=end_service_date_prop)
    )

    # Start timestamp property
    dataset_data.append(
        wbi_core.String(value=metadata.start_timestamp, prop_nr=start_timestamp_prop)
    )

    # End timestamp property
    dataset_data.append(
        wbi_core.String(value=metadata.end_timestamp, prop_nr=end_timestamp_prop)
    )

    # MD5 hash property
    dataset_data.append(wbi_core.String(value=metadata.md5_hash, prop_nr=md5_hash_prop))

    # Bounding box property
    for order_key, corner_value in metadata.bounding_box.items():
        dataset_data.append(
            create_geographical_property(order_key, corner_value, bounding_box_prop)
        )

    # Bounding octagon property
    for order_key, corner_value in metadata.bounding_octagon.items():
        dataset_data.append(
            create_geographical_property(order_key, corner_value, bounding_octagon_prop)
        )

    # Number of stops property
    dataset_data.append(
        wbi_core.Quantity(
            quantity=metadata.stops_count_by_type.get(STOP_KEY),
            prop_nr=num_of_stops_prop,
        )
    )

    # Number of stations property
    dataset_data.append(
        wbi_core.Quantity(
            quantity=metadata.stops_count_by_type.get(STATION_KEY),
            prop_nr=num_of_stations_prop,
        )
    )

    # Number of entrances property
    dataset_data.append(
        wbi_core.Quantity(
            quantity=metadata.stops_count_by_type.get(ENTRANCE_KEY),
            prop_nr=num_of_entrances_prop,
        )
    )

    # Number of agencies property
    dataset_data.append(
        wbi_core.Quantity(
            quantity=metadata.agencies_count, prop_nr=num_of_agencies_prop
        )
    )

    # Number of stops property
    for route_key, route_value in metadata.routes_count_by_type.items():
        route_qualifier = [
            wbi_core.String(value=route_key, prop_nr=route_type_prop, is_qualifier=True)
        ]
        dataset_data.append(
            wbi_core.Quantity(
                quantity=route_value,
                prop_nr=num_of_routes_prop,
                qualifiers=route_qualifier,
            )
        )

    # Dataset version entity label
    version_name_label = metadata.dataset_version_name

    metadata.dataset_version_entity_code = import_entity(
        username, password, dataset_data, version_name_label
    )

    version_prop = wbi_core.ItemID(
        value=metadata.dataset_version_entity_code,
        prop_nr=dataset_version_prop,
        if_exists=APPEND,
    )
    source_data = [version_prop]
    metadata.source_entity_code = import_entity(
        username,
        password,
        source_data,
        item_id=metadata.source_entity_code,
    )

    return gtfs_representation
