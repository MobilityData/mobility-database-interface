from usecase.process_service_date_for_gtfs_metadata import (
    process_start_service_date_for_gtfs_metadata,
    process_end_service_date_for_gtfs_metadata,
    SERVICE_DATE_NOTICES,
)
from usecase.process_timestamp_for_gtfs_metadata import (
    process_start_timestamp_for_gtfs_metadata,
    process_end_timestamp_for_gtfs_metadata,
    TIMESTAMP_NOTICES,
)
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
    MAIN_LANGUAGE_NOTICES,
)
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
    TIMEZONE_NOTICES,
)
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_box_for_gtfs_metadata,
    process_bounding_octagon_for_gtfs_metadata,
    GEO_BOUNDARIES_NOTICES,
)
from usecase.process_agencies_count_for_gtfs_metadata import (
    process_agencies_count_for_gtfs_metadata,
    AGENCIES_COUNT_NOTICES,
)
from usecase.process_routes_count_by_type_for_gtfs_metadata import (
    process_routes_count_by_type_for_gtfs_metadata,
    ROUTES_COUNT_NOTICES,
)
from usecase.process_stops_count_by_type_for_gtfs_metadata import (
    process_stops_count_by_type_for_gtfs_metadata,
    STOPS_COUNT_NOTICES,
)

SERVICE_DATE_USE_CASES = "service_date_use_cases"
TIMESTAMP_USE_CASES = "timestamp_use_cases"
MAIN_LANGUAGE_USE_CASES = "main_language_use_cases"
TIMEZONE_USE_CASES = "timezone_use_cases"
GEO_BOUNDARIES_USE_CASES = "geo_boundaries_use_cases"
AGENCIES_COUNT_USE_CASES = "agencies_count_use_cases"
ROUTES_COUNT_USE_CASES = "routes_count_use_cases"
STOPS_COUNT_USE_CASES = "stops_count_use_cases"

SCENARIO = {
    SERVICE_DATE_USE_CASES: (
        SERVICE_DATE_NOTICES,
        [
            process_start_service_date_for_gtfs_metadata,
            process_end_service_date_for_gtfs_metadata,
        ],
    ),
    TIMESTAMP_USE_CASES: (
        TIMESTAMP_NOTICES,
        [
            process_start_timestamp_for_gtfs_metadata,
            process_end_timestamp_for_gtfs_metadata,
        ],
    ),
    MAIN_LANGUAGE_USE_CASES: (
        MAIN_LANGUAGE_NOTICES,
        [process_main_language_code_for_gtfs_metadata],
    ),
    TIMEZONE_USE_CASES: (TIMEZONE_NOTICES, [process_timezones_for_gtfs_metadata]),
    GEO_BOUNDARIES_USE_CASES: (
        GEO_BOUNDARIES_NOTICES,
        [
            process_bounding_box_for_gtfs_metadata,
            process_bounding_octagon_for_gtfs_metadata,
        ],
    ),
    AGENCIES_COUNT_USE_CASES: (
        AGENCIES_COUNT_NOTICES,
        [process_agencies_count_for_gtfs_metadata],
    ),
    ROUTES_COUNT_USE_CASES: (
        ROUTES_COUNT_NOTICES,
        [process_routes_count_by_type_for_gtfs_metadata],
    ),
    STOPS_COUNT_USE_CASES: (
        STOPS_COUNT_NOTICES,
        [process_stops_count_by_type_for_gtfs_metadata],
    ),
}
