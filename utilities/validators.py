from utilities.constants import (
    PRODUCTION_SPARQL_BIGDATA_URL,
    STAGING_SPARQL_BIGDATA_URL,
    PRODUCTION_API_URL,
    STAGING_API_URL,
)
from representation.dataset_infos import DatasetInfos
from representation.gtfs_representation import GtfsRepresentation


def validate_sparql_bigdata_url(sparql_url):
    if sparql_url not in [PRODUCTION_SPARQL_BIGDATA_URL, STAGING_SPARQL_BIGDATA_URL]:
        raise TypeError(
            f"sparql_bigdata_url should be {PRODUCTION_SPARQL_BIGDATA_URL} or {STAGING_SPARQL_BIGDATA_URL}"
        )
    return True


def validate_api_url(api_url):
    if api_url not in [PRODUCTION_API_URL, STAGING_API_URL]:
        raise TypeError(f"api_url should be {PRODUCTION_API_URL} or {STAGING_API_URL}")
    return True


def validate_gtfs_representation(gtfs_representation):
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    return True


def validate_datasets_infos(datasets_infos):
    if not all(isinstance(item, DatasetInfos) for item in datasets_infos):
        raise TypeError("Datasets infos must be a valid DatasetInfos list.")
    return True
