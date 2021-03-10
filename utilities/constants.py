# Entity codes from the Mobility database
GTFS_CATALOG_OF_SOURCES_CODE = "Q78"
GBFS_CATALOG_OF_SOURCES_CODE = "Q86"
GTFS_SCHEDULE_DATA_FORMAT = "Q29"

# Properties from the Mobility database
INSTANCE_PROP = "P20"
SOURCE_ENTITY_PROP = "P48"
MAIN_TIMEZONE_PROP = "P49"
MAIN_LANGUAGE_CODE_PROP = "P54"
START_SERVICE_DATE_PROP = "P52"
END_SERVICE_DATE_PROP = "P53"
START_TIMESTAMP_PROP = "P66"
END_TIMESTAMP_PROP = "P67"
MD5_HASH_PROP = "P61"
DATASET_VERSION_PROP = "P64"
STABLE_URL_PROP = "P55"

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

SPARQL_A = "a"
SVC_SOURCE_PROPERTY_URL = "http://wikibase.svc/prop/statement/P48"
SVC_CATALOG_PROPERTY_URL = "http://wikibase.svc/prop/statement/P65"
SVC_ENTITY_URL_PREFIX = "http://wikibase.svc/entity/"
SVC_URL = "http://wikibase.svc"
