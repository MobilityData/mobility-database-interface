import base64
import json
import os
import sys

from google import pubsub_v1
from google.pubsub_v1 import PubsubMessage
from wikibaseintegrator import wbi_core, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config

from repository.data_repository import DataRepository
from representation.dataset_infos import DatasetInfos
from representation.dataset_representation_factory import GTFS_TYPE
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_dataset_entity_for_gtfs_metadata,
)
from usecase.download_dataset_as_zip import download_dataset_as_zip
from usecase.load_dataset import load_dataset
from usecase.process_agencies_count_for_gtfs_metadata import (
    process_agencies_count_for_gtfs_metadata,
)
from usecase.process_geopraphical_boundaries_for_gtfs_metadata import (
    process_bounding_box_for_gtfs_metadata,
    process_bounding_octagon_for_gtfs_metadata,
)
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
)
from usecase.process_routes_count_by_type_for_gtfs_metadata import (
    process_routes_count_by_type_for_gtfs_metadata,
)
from usecase.process_service_date_for_gtfs_metadata import (
    process_start_service_date_for_gtfs_metadata,
    process_end_service_date_for_gtfs_metadata,
)
from usecase.process_sha1 import process_sha1
from usecase.process_stops_count_by_type_for_gtfs_metadata import (
    process_stops_count_by_type_for_gtfs_metadata,
)
from usecase.process_timestamp_for_gtfs_metadata import (
    process_start_timestamp_for_gtfs_metadata,
    process_end_timestamp_for_gtfs_metadata,
)
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
)
from utilities.constants import (
    API_URL,
    SVC_URL,
    SPARQL_BIGDATA_URL,
    STAGING_API_URL,
    STAGING_SPARQL_BIGDATA_URL,
    USERNAME,
    PASSWORD,
    INSTANCE_PROP,
    GTFS_SCHEDULE_SOURCE_CODE,
    STABLE_URL_PROP,
    CATALOG_PROP,
    GTFS_CATALOG_OF_SOURCES_CODE,
    LABELS,
    ENGLISH,
    VALUE,
    SOURCE_NAME,
    DATASET_URL,
    SOURCE_ENTITY_ID,
    GOOGLE_CLOUD_PROJECT,
    TOPIC_DISPATCHER,
    DATATYPE,
    SOURCE_ENTITY_PROP,
    APPEND,
)


def decode_message(event):
    if "data" not in event:
        return None
    json_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(json_message)
    return message


def add_dataset_to_source(
    source_name, dataset_url, source_entity_id, data_type, username, password
):
    # Load Wikibase Integrator config with the environment
    api_url = os.getenv(API_URL, STAGING_API_URL)
    wbi_config["MEDIAWIKI_API_URL"] = api_url
    wbi_config["SPARQL_ENDPOINT_URL"] = os.getenv(
        SPARQL_BIGDATA_URL, STAGING_SPARQL_BIGDATA_URL
    )
    wbi_config["WIKIBASE_URL"] = SVC_URL

    # Initialize DataRepository
    data_repository = DataRepository()

    dataset_infos = DatasetInfos()
    dataset_infos.source_name = source_name
    dataset_infos.url = dataset_url
    dataset_infos.entity_code = source_entity_id
    # Download datasets zip file
    dataset_infos = download_dataset_as_zip(f"/tmp/{source_name}", dataset_infos)

    # Process the MD5 hash
    dataset_infos = process_sha1(dataset_infos)

    # Load the datasets in memory in the data repository
    data_repository = load_dataset(data_repository, dataset_infos, data_type)

    # Process each dataset representation in the data_repository
    dataset_representations = []
    for (
        dataset_key,
        dataset_representation,
    ) in data_repository.get_dataset_representations().items():
        dataset_representation = process_start_service_date_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_end_service_date_for_gtfs_metadata(
            dataset_representation
        )
        # TODO: fix the actual issue. might be taken care of once validator is deployed.
        try:
            dataset_representation = process_start_timestamp_for_gtfs_metadata(
                dataset_representation
            )
        except TypeError as te:
            print(
                f"process_start_timestamp_for_gtfs_metadata for source {source_name}, dataset {dataset_url} raised: \n {te}",
                file=sys.stderr,
            )
        try:
            dataset_representation = process_end_timestamp_for_gtfs_metadata(
                dataset_representation
            )
        except TypeError as te:
            print(
                f"process_end_timestamp_for_gtfs_metadata for source {source_name}, dataset {dataset_url} raised: \n {te}",
                file=sys.stderr,
            )
        dataset_representation = process_main_language_code_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_timezones_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_bounding_box_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_bounding_octagon_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_agencies_count_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_routes_count_by_type_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = process_stops_count_by_type_for_gtfs_metadata(
            dataset_representation
        )
        dataset_representation = create_dataset_entity_for_gtfs_metadata(
            dataset_representation, api_url, username, password
        )
        dataset_representations.append(dataset_representation)
    return dataset_representations


class SourceAlreadyExistException(Exception):
    def __init__(self, stable_url):
        self.message = f"source with stable url: {stable_url} already exists"


def add_source_in_db(source_name, stable_url, username=None, password=None):
    """"""
    # Load Wikibase Integrator config with the environment
    wbi_config["MEDIAWIKI_API_URL"] = os.environ[API_URL]
    wbi_config["SPARQL_ENDPOINT_URL"] = os.environ[SPARQL_BIGDATA_URL]
    wbi_config["WIKIBASE_URL"] = SVC_URL

    if not username:
        username = os.environ[USERNAME]
    if not password:
        password = os.environ[PASSWORD]
    stable_url_prop = os.environ[STABLE_URL_PROP]
    catalog_prop = os.environ[CATALOG_PROP]

    login_instance = wbi_login.Login(
        user=username,
        pwd=password,
    )

    source_instance_of = wbi_core.ItemID(
        prop_nr=os.environ[INSTANCE_PROP], value=os.environ[GTFS_SCHEDULE_SOURCE_CODE]
    )
    source_stable_url = wbi_core.Url(value=stable_url, prop_nr=stable_url_prop)
    source_catalog_ref = wbi_core.ItemID(
        prop_nr=catalog_prop,
        value=os.environ[GTFS_CATALOG_OF_SOURCES_CODE],  # fix this
    )
    source_catalog_entity = wbi_core.ItemEngine(
        item_id=os.environ[GTFS_CATALOG_OF_SOURCES_CODE]
    )
    source_catalog_entity_json = source_catalog_entity.get_json_representation()

    source_data = [source_instance_of, source_stable_url, source_catalog_ref]
    source_entity = wbi_core.ItemEngine(data=source_data, core_props={stable_url_prop})

    # TODO: uncomment this
    # if source_entity.item_id:
    #     raise SourceAlreadyExistException(stable_url=stable_url)
    cleaned_source_name = source_name.replace(GTFS_TYPE, "").strip()
    source_entity.set_label(cleaned_source_name)

    source_entity_id = source_entity.write(login=login_instance)
    source_entity_prop = wbi_core.ItemID(
        value=source_entity_id, prop_nr=os.environ[SOURCE_ENTITY_PROP], if_exists=APPEND
    )
    catalog_data = [source_entity_prop]
    source_catalog_entity.update(catalog_data)
    source_catalog_entity.write(login_instance)

    return source_entity_id


def add_source_and_dispatch(
    source_name, stable_url, versions, datatype, username, password
):
    publisher = pubsub_v1.PublisherClient()
    source_entity_id = add_source_in_db(source_name, stable_url, username, password)

    for dataset_version_url in reversed(versions):
        # adding old datasets first
        message = {
            SOURCE_NAME: source_name,
            DATASET_URL: dataset_version_url,
            SOURCE_ENTITY_ID: source_entity_id,
            DATATYPE: datatype,
        }
        publish_dispatcher_message(publisher, message)
    message = {
        SOURCE_NAME: source_name,
        DATASET_URL: stable_url,
        SOURCE_ENTITY_ID: source_entity_id,
        DATATYPE: datatype,
    }
    publish_dispatcher_message(publisher, message)
    return source_entity_id


def publish_message(publisher, topic_name, message):
    project_id = os.environ[GOOGLE_CLOUD_PROJECT]
    if not topic_name:
        raise Exception(
            f"env var TOPIC_DISPATCHER is badly set. It's current value is: {topic_name}"
        )
    if not project_id:
        raise Exception(
            f"env var GOOGLE_CLOUD_PROJECT is badly set. It's current value is: {project_id}"
        )
    topic_path = f"projects/{project_id}/topics/{topic_name}"

    message_json = json.dumps(message)
    encoded_message = message_json.encode("utf-8")
    message_obj = PubsubMessage(data=encoded_message)
    future = publisher.publish(topic=topic_path, messages=[message_obj])
    try:
        return future.result()
    except AttributeError as ae:
        print(f"AttributeError on future.result. future is {future}")


def publish_dispatcher_message(publisher, message):
    topic_name = os.environ[TOPIC_DISPATCHER]
    published = publish_message(publisher, topic_name, message)
    return published
