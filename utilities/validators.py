from utilities.constants import (
    PRODUCTION_SPARQL_URL,
    STAGING_SPARQL_URL,
    PRODUCTION_API_URL,
    STAGING_API_URL,
)
from representation.gtfs_representation import GtfsRepresentation


def validate_sparql_url(sparql_url):
    if sparql_url not in [PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL]:
        raise TypeError(
            f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}"
        )
    return True


def validate_api_url(api_url):
    if api_url not in [PRODUCTION_API_URL, STAGING_API_URL]:
        raise TypeError(
            f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}"
        )
    return True


def validate_gtfs_representation(gtfs_representation):
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    return True
