# Entity codes from the Mobility database
GTFS_CATALOG_OF_SOURCES_CODE = "Q78"
GBFS_CATALOG_OF_SOURCES_CODE = "Q86"

# Define regex pattern for dataset version entity code in response retrieved by SPARQL query
SPARQL_ENTITY_CODE_REGEX = "/(Q.+?)-"

# External constants
STAGING_SPARQL_URL = (
    "http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
PRODUCTION_SPARQL_URL = (
    "http://mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
STAGING_API_URL = "http://staging.mobilitydatabase.org/w/api.php"
PRODUCTION_API_URL = "http://mobilitydatabase.org/w/api.php"

ACTION = "action"
WB_GET_ENTITIES = "wbgetentities"
IDS = "ids"
LANGUAGES = "languages"
FORMAT = "format"
ENTITIES = "entities"
CLAIMS = "claims"
MAINSNAK = "mainsnak"
DATAVALUE = "datavalue"
VALUE = "value"
RESULTS = "results"
BINDINGS = "bindings"
LABELS = "labels"
ENGLISH = "en"
