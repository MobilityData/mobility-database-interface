import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import secretmanager

from helpers_cf import (
    decode_message,
    add_source_and_dispatch,
    add_dataset_to_source,
)
from usecase.load_dataset import GBFS_TYPE, GTFS_TYPE
from utilities.constants import (
    SOURCE_NAME,
    STABLE_URL,
    VERSIONS,
    DATASET_URL,
    SOURCE_ENTITY_ID,
    DATATYPE,
    SECRET_PATH,
    PASSWORD_LOWERCASE,
    USERNAME_LOWERCASE,
)

BASE_DIR = Path(__file__).resolve().parent


def add_new_source_cf(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    This Cloud Function adds a new source in the database
    and publishes several messages (as many as there are dataset versions + stable url version)
    in the before-dispatcher topic.

     It takes a message of the following structure:
     {
         "soure_name": "somestr",
         "stable_url": "someurl",
         "versions": [ "someurl", "someurl", ... ],
         "datatype": "somestr"
    }

     Args:
          event (dict):
             The dictionary with data specific to this type of
          event.
             The `data` field contains the PubsubMessage message.
             The `attributes` field will contain custom attributes if there are any.
          context (google.cloud.functions.Context):
             The Cloud Functions event metadata.
             The `event_id` field contains the Pub/Sub message ID.
             The `timestamp` field contains the publish time.
    """
    if os.getenv("ENV") == "prod":
        load_dotenv(f"{BASE_DIR}/.env.production")
    else:
        load_dotenv(f"{BASE_DIR}/.env.staging")

    message = decode_message(event)
    source_name = message[SOURCE_NAME]
    stable_url = message[STABLE_URL]
    versions = message[VERSIONS]
    datatype = message[DATATYPE]

    client = secretmanager.SecretManagerServiceClient()
    credentials = client.access_secret_version(
        request={"name": f"{os.getenv(SECRET_PATH)}/versions/latest"}
    )
    decoded_credentials_str = credentials.payload.data.decode("utf_8")
    json_creds = json.loads(decoded_credentials_str)
    username = json_creds[USERNAME_LOWERCASE]
    password = json_creds[PASSWORD_LOWERCASE]

    source_entity_id = add_source_and_dispatch(
        source_name, stable_url, versions, datatype, username, password
    )
    return source_entity_id


def add_dataset_to_source_cf(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    This Cloud Function adds a new source in the database
    and publishes several messages (as many as there are dataset versions + stable url version)
    in the before-dispatcher topic.

     It takes a message of the following structure:
     {
         "soure_name": "somestr",
         "dataset_url": "someurl",
         "source_entity_id": "someentityid"
         "datatype": "somedatatype" # must be GTFS or GBFS
    }

     Args:
          event (dict):
             The dictionary with data specific to this type of
          event.
             The `data` field contains the PubsubMessage message.
             The `attributes` field will contain custom attributes if there are any.
          context (google.cloud.functions.Context):
             The Cloud Functions event metadata.
             The `event_id` field contains the Pub/Sub message ID.
             The `timestamp` field contains the publish time.
    """
    if os.getenv("ENV") == "prod":
        load_dotenv(f"{BASE_DIR}/.env.production")
    else:
        load_dotenv(f"{BASE_DIR}/.env.staging")

    message = decode_message(event)

    source_name = message[SOURCE_NAME]
    dataset_url = message[DATASET_URL]
    source_entity_id = message[SOURCE_ENTITY_ID]
    dataset_data_type = message[DATATYPE]
    if dataset_data_type not in [GTFS_TYPE, GBFS_TYPE]:
        raise Exception(f"{dataset_data_type} is invalid")

    client = secretmanager.SecretManagerServiceClient()
    credentials = client.access_secret_version(
        request={"name": f"{os.getenv(SECRET_PATH)}/versions/latest"}
    )
    decoded_credentials_str = credentials.payload.data.decode("utf_8")
    json_creds = json.loads(decoded_credentials_str)
    username = json_creds[USERNAME_LOWERCASE]
    password = json_creds[PASSWORD_LOWERCASE]

    add_dataset_to_source(
        source_name,
        dataset_url,
        source_entity_id,
        dataset_data_type,
        username,
        password,
    )
