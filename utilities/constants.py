# Entity codes from the Mobility database
GTFS_CATALOG_OF_SOURCES_CODE = "Q78"
GBFS_CATALOG_OF_SOURCES_CODE = "Q86"
GTFS_SCHEDULE_DATA_FORMAT = "Q29"

# Properties from the Mobility database
INSTANCE_PROP = "P20"
SOURCE_ENTITY_PROP = "P48"
TIMEZONE_PROP = "P49"
MAIN_LANGUAGE_CODE_PROP = "P54"
START_SERVICE_DATE_PROP = "P52"
END_SERVICE_DATE_PROP = "P53"
START_TIMESTAMP_PROP = "P66"
END_TIMESTAMP_PROP = "P67"
MD5_HASH_PROP = "P61"
DATASET_VERSION_PROP = "P64"
STABLE_URL_PROP = "P55"
ORDER_PROP = "P38"
BOUNDING_BOX_PROP = "P63"
BOUNDING_OCTAGON_PROP = "P68"
NUM_OF_STOPS_PROP = "P69"
NUM_OF_STATIONS_PROP = "P70"
NUM_OF_ENTRANCES_PROP = "P71"
NUM_OF_AGENCIES_PROP = "P72"
NUM_OF_ROUTES_PROP = "P73"
ROUTE_TYPE_PROP = "P74"

# Define regex pattern for dataset version entity code in response retrieved by SPARQL query
SPARQL_ENTITY_CODE_REGEX = "/(Q.+?)-"

# External constants
STAGING_SPARQL_URL = (
    "http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
PRODUCTION_SPARQL_URL = (
    "http://mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
STAGING_SPARQL_BIGDATA_URL = "http://staging.mobilitydatabase.org:8989/bigdata/sparql"
PRODUCTION_SPARQL_BIGDATA_URL = "http://mobilitydatabase.org:8989/bigdata/sparql"
STAGING_API_URL = "http://staging.mobilitydatabase.org/w/api.php"
PRODUCTION_API_URL = "http://mobilitydatabase.org/w/api.php"

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
SVC_SOURCE_PROPERTY_URL = "http://wikibase.svc/prop/statement/P48"
SVC_CATALOG_PROPERTY_URL = "http://wikibase.svc/prop/statement/P65"
SVC_ENTITY_URL_PREFIX = "http://wikibase.svc/entity/"
SVC_URL = "http://wikibase.svc"
