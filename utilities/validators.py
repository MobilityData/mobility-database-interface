from utilities.constants import (
    PRODUCTION_SPARQL_URL,
    STAGING_SPARQL_URL,
    PRODUCTION_API_URL,
    STAGING_API_URL,
)
from representation.dataset_infos import DatasetInfos
from representation.gtfs_representation import GtfsRepresentation


def validate_sparql_url(sparql_url):
    if sparql_url not in [PRODUCTION_SPARQL_URL, STAGING_SPARQL_URL]:
        raise TypeError(
            f"sparql_api should be {PRODUCTION_SPARQL_URL} or {STAGING_SPARQL_URL}"
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


def validate_report(report):
    notices = report.get("notices", None)
    if notices is None:
        raise Exception("The report is invalid, does not contain notices.")
    for notice_type in notices:
        notice_code = notice_type.get("code", None)
        if notice_code is None or len(notice_code) == 0:
            raise Exception("The report is invalid, notice codes must be defined.")
        notice_instances = notice_type.get("notices", None)
        if notice_instances is None or len(notice_instances) == 0:
            raise Exception(
                "The report is invalid, a notice type must have notice instances."
            )
        for notice_instance in notice_instances:
            if len(notice_instance) == 0:
                raise Exception(
                    "The report is invalid, a notice instance must not be empty."
                )
    return True
