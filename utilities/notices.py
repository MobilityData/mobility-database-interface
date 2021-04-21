#####################################
# Notice types
#####################################

STANDALONE = "standalone"
WITH_FILENAME = "with_filename"


#####################################
# Filenames
#####################################

FILENAME = "filename"
AGENCY_TXT = "agency.txt"
STOPS_TXT = "stops.txt"
ROUTES_TXT = "routes.txt"
TRIPS_TXT = "trips.txt"
STOP_TIMES_TXT = "stop_times.txt"
CALENDAR_TXT = "calendar.txt"
CALENDAR_DATES_TXT = "calendar_dates.txt"
FARE_RULES_TXT = "fare_rules.txt"
SHAPES_TXT = "shapes.txt"
FREQUENCIES_TXT = "frequencies.txt"
FEED_INFO_TXT = "feed_info.txt"


#####################################
# Keys used in both reports
#####################################

REPORT_NOTICES_TYPE = "notices"
REPORT_NOTICES = "notices"
REPORT_CODE = "code"
REPORT_FILENAME = "filename"
REPORT_CHILD_FILENAME = "childFilename"


#####################################
# Standalone validation error notices
#####################################

# agency.txt
INCONSISTENT_AGENCY_TIMEZONE = "inconsistent_agency_timezone"

# stops.txt
STATION_WITH_PARENT_STATION = "station_with_parent_station"
LOCATION_WITHOUT_PARENT_STATION = "location_without_parent_station"
WRONG_PARENT_LOCATION_TYPE = "wrong_parent_location_type"

# routes.txt
ROUTE_BOTH_SHORT_AND_LONG_NAME_MISSING = "route_both_short_and_long_name_missing"

# trips.txt, stop_times.txt, calendar.txt and calendar_dates.txt
BLOCK_TRIPS_WITH_OVERLAPPING_STOP_TIMES = "block_trips_with_overlapping_stop_times"

# stop_times.txt
STOP_TIME_WITH_ONLY_ARRIVAL_OR_DEPARTURE_TIME = (
    "stop_time_with_only_arrival_or_departure_time"
)
STOP_TIME_WITH_ARRIVAL_BEFORE_PREVIOUS_DEPARTURE_TIME = (
    "stop_time_with_arrival_before_previous_departure_time"
)
DECREASING_OR_EQUAL_STOP_TIME_DISTANCE = "decreasing_or_equal_stop_time_distance"
MISSING_TRIP_EDGE = "missing_trip_edge"

# calendar.txt and calendar_dates.txt
MISSING_CALENDAR_AND_CALENDAR_DATE_FILES = "missing_calendar_and_calendar_date_files"

# fare_rules.txt
DUPLICATE_FARE_RULE_ZONE_ID_FIELDS = "duplicate_fare_rule_zone_id_fields"

# shapes.txt
DECREASING_OR_EQUAL_SHAPE_DISTANCE = "decreasing_or_equal_shape_distance"

# frequencies.txt
OVERLAPPING_FREQUENCY = "overlapping_frequency"


########################################
# Validation error notices with filename
########################################
DUPLICATED_COLUMN = "duplicated_column"
DUPLICATE_KEY = "duplicate_key"
EMPTY_FILE = "empty_file"
INVALID_COLOR = "invalid_color"
INVALID_CURRENCY = "invalid_currency"
INVALID_DATE = "invalid_date"
INVALID_EMAIL = "invalid_email"
INVALID_FLOAT = "invalid_float"
INVALID_INTEGER = "invalid_integer"
INVALID_LANGUAGE_CODE = "invalid_language_code"
INVALID_PHONE_NUMBER = "invalid_phone_number"
INVALID_ROW_LENGTH = "invalid_row_length"
INVALID_TIME = "invalid_time"
INVALID_TIMEZONE = "invalid_timezone"
INVALID_URL = "invalid_url"
LEADING_OR_TRAILING_WHITESPACES = "leading_or_trailing_whitespaces"
MISSING_REQUIRED_COLUMN = "missing_required_column"
MISSING_REQUIRED_FIELD = "missing_required_field"
MISSING_REQUIRED_FILE = "missing_required_file"
NEW_LINE_IN_VALUE = "new_line_in_value"
NUMBER_OUT_OF_RANGE = "number_out_of_range"
START_AND_END_RANGE_OUT_OF_ORDER = "start_and_end_range_out_of_order"
START_AND_END_RANGE_EQUAL = "start_and_end_range_equal"
SAME_NAME_AND_DESCRIPTION_FOR_ROUTE = "same_name_and_description_for_route"


#########################################################
# Validation error notices were child file is problematic
#########################################################
FOREIGN_KEY_VIOLATION = "foreign_key_violation"


#################################
# Standalone system error notices
#################################
IO_ERROR = "i_o_error"
THREAD_EXECUTION_ERROR = "thread_execution_error"
THREAD_INTERRUPTED_ERROR = "thread_interrupted_error"
URI_SYNTAX_ERROR = "u_r_i_syntax_error"


####################################
# System error notices with filename
####################################
RUNTIME_EXCEPTION_IN_LOADER_ERROR = "runtime_exception_in_loader_error"


###############################################
# System error notices with validator classname
# NB. Will be treated as standalone for now
###############################################
RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR = "runtime_exception_in_validator_error"


###############################################
# Use case problematic notices
###############################################
AGENCIES_COUNT_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {AGENCY_TXT},
}

GEO_BOUNDARIES_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_FLOAT,
        INVALID_ROW_LENGTH,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {STOPS_TXT},
}

MAIN_LANGUAGE_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_LANGUAGE_CODE,
        INVALID_ROW_LENGTH,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {AGENCY_TXT},
}

ROUTES_COUNT_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_INTEGER,
        INVALID_ROW_LENGTH,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {ROUTES_TXT},
}

SERVICE_DATE_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        MISSING_CALENDAR_AND_CALENDAR_DATE_FILES,
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_DATE,
        INVALID_ROW_LENGTH,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        START_AND_END_RANGE_OUT_OF_ORDER,
        START_AND_END_RANGE_EQUAL,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {FEED_INFO_TXT, CALENDAR_TXT, CALENDAR_DATES_TXT},
}

STOPS_COUNT_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        STATION_WITH_PARENT_STATION,
        LOCATION_WITHOUT_PARENT_STATION,
        WRONG_PARENT_LOCATION_TYPE,
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_INTEGER,
        INVALID_ROW_LENGTH,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {STOPS_TXT},
}

TIMESTAMP_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        MISSING_CALENDAR_AND_CALENDAR_DATE_FILES,
        BLOCK_TRIPS_WITH_OVERLAPPING_STOP_TIMES,
        STOP_TIME_WITH_ONLY_ARRIVAL_OR_DEPARTURE_TIME,
        STOP_TIME_WITH_ARRIVAL_BEFORE_PREVIOUS_DEPARTURE_TIME,
        MISSING_TRIP_EDGE,
        INCONSISTENT_AGENCY_TIMEZONE,
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_DATE,
        INVALID_ROW_LENGTH,
        INVALID_TIME,
        INVALID_TIMEZONE,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        NUMBER_OUT_OF_RANGE,
        START_AND_END_RANGE_OUT_OF_ORDER,
        START_AND_END_RANGE_EQUAL,
        FOREIGN_KEY_VIOLATION,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {CALENDAR_TXT, CALENDAR_DATES_TXT, STOP_TIMES_TXT, TRIPS_TXT, AGENCY_TXT},
}

TIMEZONE_FOR_GTFS_METADATA_NOTICES = {
    STANDALONE: {
        INCONSISTENT_AGENCY_TIMEZONE,
        IO_ERROR,
        THREAD_EXECUTION_ERROR,
        THREAD_INTERRUPTED_ERROR,
        URI_SYNTAX_ERROR,
        RUNTIME_EXCEPTION_IN_VALIDATOR_ERROR,
    },
    WITH_FILENAME: {
        DUPLICATED_COLUMN,
        DUPLICATE_KEY,
        EMPTY_FILE,
        INVALID_ROW_LENGTH,
        INVALID_TIMEZONE,
        LEADING_OR_TRAILING_WHITESPACES,
        MISSING_REQUIRED_COLUMN,
        MISSING_REQUIRED_FIELD,
        MISSING_REQUIRED_FILE,
        NEW_LINE_IN_VALUE,
        RUNTIME_EXCEPTION_IN_LOADER_ERROR,
    },
    FILENAME: {AGENCY_TXT, STOPS_TXT},
}
