from utilities.constants import PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL, PRODUCTION_API_URL, STAGING_API_URL


def validate_urls(api_url, sparql_api):
    if sparql_api not in [PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL]:
        raise TypeError(f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}")
    if api_url not in [PRODUCTION_API_URL, STAGING_API_URL]:
        raise TypeError(f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}")

