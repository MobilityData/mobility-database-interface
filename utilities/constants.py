# Project constants
ID = "id"
CLAIMS = "claims"
MAINSNAK = "mainsnak"
DATAVALUE = "datavalue"
VALUE = "value"
RESULTS = "results"
BINDINGS = "bindings"
LABELS = "labels"
ENGLISH = "en"
DATATYPE = "datatype"
RANK = "rank"
PROP_ID = "prop_id"
IF_EXISTS = "if_exists"
NORMAL = "normal"
PREFERRED = "preferred"
GLOBE_PRECISION = 1.0e-6
GLOBE_URL = "http://www.wikidata.org/entity/Q2"
LAT = "latitude"
LON = "longitude"
REPLACE = "REPLACE"
APPEND = "APPEND"

STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"
IS_ADDITION = "is_addition"
IS_MAXIMUM = "is_maximum"

STOP_KEY = "stop"
STATION_KEY = "station"
ENTRANCE_KEY = "entrance"
STOP = 0
STATION = 1
ENTRANCE = 2
LOCATION_TYPE = "location_type"

SPARQL_A = "a"
SVC_PROP_URL_PATH = "/prop/statement/"
SVC_ENTITY_URL_PATH = "/entity/"
SVC_URL = "http://wikibase.svc"

# Define regex pattern for dataset version entity code in response retrieved by SPARQL query
SPARQL_ENTITY_CODE_REGEX = "/(Q.+?)-"

# Possible URLs for SPARQL and API
STAGING_SPARQL_URL = (
    "http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
STAGING_SPARQL_BIGDATA_URL = "http://staging.mobilitydatabase.org:8989/bigdata/sparql"
STAGING_API_URL = "http://staging.mobilitydatabase.org/w/api.php"
PRODUCTION_SPARQL_URL = (
    "http://mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
PRODUCTION_SPARQL_BIGDATA_URL = "http://mobilitydatabase.org:8989/bigdata/sparql"
PRODUCTION_API_URL = "http://mobilitydatabase.org/w/api.php"

# Environment variables keys
GTFS_CATALOG_OF_SOURCES_CODE = "GTFS_CATALOG_OF_SOURCES_CODE"
GBFS_CATALOG_OF_SOURCES_CODE = "GBFS_CATALOG_OF_SOURCES_CODE"
GTFS_SCHEDULE_DATA_FORMAT = "GTFS_SCHEDULE_DATA_FORMAT"

INSTANCE_PROP = "INSTANCE_PROP"
SOURCE_ENTITY_PROP = "SOURCE_ENTITY_PROP"
TIMEZONE_PROP = "TIMEZONE_PROP"
MAIN_LANGUAGE_CODE_PROP = "MAIN_LANGUAGE_CODE_PROP"
START_SERVICE_DATE_PROP = "START_SERVICE_DATE_PROP"
END_SERVICE_DATE_PROP = "END_SERVICE_DATE_PROP"
START_TIMESTAMP_PROP = "START_TIMESTAMP_PROP"
END_TIMESTAMP_PROP = "END_TIMESTAMP_PROP"
MD5_HASH_PROP = "MD5_HASH_PROP"
DATASET_VERSION_PROP = "DATASET_VERSION_PROP"
STABLE_URL_PROP = "STABLE_URL_PROP"
ORDER_PROP = "ORDER_PROP"
BOUNDING_BOX_PROP = "BOUNDING_BOX_PROP"
BOUNDING_OCTAGON_PROP = "BOUNDING_OCTAGON_PROP"
NUM_OF_STOPS_PROP = "NUM_OF_STOPS_PROP"
NUM_OF_STATIONS_PROP = "NUM_OF_STATIONS_PROP"
NUM_OF_ENTRANCES_PROP = "NUM_OF_ENTRANCES_PROP"
NUM_OF_AGENCIES_PROP = "NUM_OF_AGENCIES_PROP"
NUM_OF_ROUTES_PROP = "NUM_OF_ROUTES_PROP"
ROUTE_TYPE_PROP = "ROUTE_TYPE_PROP"
CATALOG_PROP = "CATALOG_PROP"
GTFS_SCHEDULE_SOURCE_CODE = "GTFS_SCHEDULE_SOURCE_CODE"

SPARQL_URL = "SPARQL_URL"
SPARQL_BIGDATA_URL = "SPARQL_BIGDATA_URL"
API_URL = "API_URL"

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

SOURCE_NAME = "source_name"
STABLE_URL = "stable_url"
DATASET_URL = "dataset_url"
SOURCE_ENTITY_ID = "source_entity_id"
VERSIONS = "versions"
