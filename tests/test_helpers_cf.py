import base64
import os
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch, Mock

from google.cloud import pubsub_v1
from google.pubsub_v1 import PubsubMessage

from helpers_cf import (
    publish_message,
    publish_dispatcher_message,
    add_source_and_dispatch,
    add_source_in_db,
    decode_message,
    add_dataset_to_source,
    SourceAlreadyExistException,
)
from usecase.load_dataset import GTFS_TYPE
from utilities.constants import (
    GOOGLE_CLOUD_PROJECT,
    TOPIC_DISPATCHER,
    API_URL,
    SPARQL_BIGDATA_URL,
    USERNAME,
    PASSWORD,
    INSTANCE_PROP,
    GTFS_SCHEDULE_SOURCE_CODE,
    STABLE_URL_PROP,
    CATALOG_PROP,
    GTFS_CATALOG_OF_SOURCES_CODE,
    DATASET_URL,
)


class PubSubTestCase(unittest.TestCase):
    @patch("helpers_cf.pubsub_v1")
    def test_publish_message(self, mock_pubsub):
        os.environ[GOOGLE_CLOUD_PROJECT] = "someprojectid"
        publisher = mock_pubsub.PublisherClient()
        topic_name = "somestr"
        message = {
            "source_name": "test_source_name",
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        publish_message(publisher, topic_name, message)
        self.assertEqual(1, publisher.publish.call_count)
        del os.environ[GOOGLE_CLOUD_PROJECT]

    @patch("helpers_cf.pubsub_v1")
    def test_publish_message_invalid_json(self, mock_pubsub):
        os.environ[GOOGLE_CLOUD_PROJECT] = "someprojectid"
        publisher = mock_pubsub.PublisherClient()
        topic_name = "somestr"
        message = {
            "source_name": datetime.now(),
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        self.assertRaises(TypeError, publish_message, publisher, topic_name, message)
        del os.environ[GOOGLE_CLOUD_PROJECT]

    @patch("helpers_cf.pubsub_v1")
    def test_publish_message_topic_name_none(self, mock_pubsub):
        os.environ[GOOGLE_CLOUD_PROJECT] = "test-project-id-123123"
        publisher = mock_pubsub.PublisherClient()
        topic_name = None
        message = {
            "source_name": "test_source_name",
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        self.assertRaises(Exception, publish_message, publisher, topic_name, message)
        del os.environ[GOOGLE_CLOUD_PROJECT]

    @patch("helpers_cf.pubsub_v1")
    def test_publish_message_project_id_none(self, mock_pubsub):
        if os.getenv(GOOGLE_CLOUD_PROJECT):
            del os.environ[GOOGLE_CLOUD_PROJECT]
        publisher = mock_pubsub.PublisherClient()
        topic_name = "somestr"
        message = {
            "source_name": "test_source_name",
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        self.assertRaises(KeyError, publish_message, publisher, topic_name, message)

    @patch("helpers_cf.pubsub_v1")
    def test_publish_message_project_id_falsy(self, mock_pubsub):
        os.environ[GOOGLE_CLOUD_PROJECT] = ""
        publisher = mock_pubsub.PublisherClient()
        topic_name = "somestr"
        message = {
            "source_name": "test_source_name",
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        self.assertRaises(Exception, publish_message, publisher, topic_name, message)
        del os.environ[GOOGLE_CLOUD_PROJECT]

    @patch("helpers_cf.pubsub_v1")
    def test_publish_dispatcher_message(self, mock_pubsub):
        publisher = mock_pubsub.PublisherClient()
        message = {
            "source_name": "test_source_name",
            "dataset_url": "someurl",
            "source_entity_id": "someid",
        }
        os.environ[GOOGLE_CLOUD_PROJECT] = "test-project-id-123123"
        os.environ[TOPIC_DISPATCHER] = "test-topic-dispatcher"
        expected_arg_message = [
            PubsubMessage(
                data=b'{"source_name": "test_source_name", "dataset_url": "someurl", "source_entity_id": "someid"}'
            )
        ]
        publish_dispatcher_message(publisher, message)
        self.assertEqual(
            "projects/test-project-id-123123/topics/test-topic-dispatcher",
            publisher.publish.call_args.kwargs["topic"],
        )
        self.assertEqual(
            expected_arg_message, publisher.publish.call_args.kwargs["messages"]
        )
        self.assertEqual(1, publisher.publish.call_count)
        del os.environ[GOOGLE_CLOUD_PROJECT]
        del os.environ[TOPIC_DISPATCHER]


class AddSourceTestCase(unittest.TestCase):
    @patch("helpers_cf.add_source_in_db")
    @patch("helpers_cf.publish_dispatcher_message")
    @patch("helpers_cf.pubsub_v1")
    def test_add_source_and_dispatch(
        self, mock_pubsub, mock_publish_dispatcher, mock_add_source_in_db
    ):

        mock_pubsub.PublisherClient = Mock()
        source_name = "some source name"
        stable_url = "some://url"
        versions = ["some://url", "some://url2", "some://url3"]

        mock_add_source_in_db.return_value = "Q1"

        source_entity_id = add_source_and_dispatch(
            source_name, stable_url, versions, GTFS_TYPE, "someusername", "somepassword"
        )
        self.assertEqual(4, mock_publish_dispatcher.call_count)
        self.assertEqual(
            "some://url3",
            mock_publish_dispatcher.call_args_list[0].args[1][DATASET_URL],
        )
        self.assertEqual("Q1", source_entity_id)

    @patch("helpers_cf.wbi_core")
    @patch("helpers_cf.wbi_login")
    def test_add_source_in_db(self, mock_wbi_login, mock_wbi_core):
        os.environ[API_URL] = "api://url"
        os.environ[SPARQL_BIGDATA_URL] = "sparql://url"
        os.environ[USERNAME] = "usrname"
        os.environ[PASSWORD] = "pwd"
        os.environ[INSTANCE_PROP] = "instanceprop"
        os.environ[GTFS_SCHEDULE_SOURCE_CODE] = "gtfsschedprop"
        os.environ[STABLE_URL_PROP] = "gtfsschedprop"
        os.environ[CATALOG_PROP] = "gtfsschedprop"
        os.environ[GTFS_CATALOG_OF_SOURCES_CODE] = "gtfsschedprop"

        mock_wbi_core.ItemEngine.return_value.write.return_value = "Q1"
        mock_wbi_core.ItemEngine.return_value.item_id = ""

        source_name = "source name"
        stable_url = "stable://url"
        source_entity_id = add_source_in_db(source_name, stable_url)
        self.assertEqual("Q1", source_entity_id)
        self.assertEqual(1, mock_wbi_login.Login.call_count)
        self.assertTrue(
            mock_wbi_core.ItemEngine.return_value.set_label.call_args_list[0]
            .args[0]
            .startswith("source name's")
        )

        del os.environ[API_URL]
        del os.environ[SPARQL_BIGDATA_URL]
        del os.environ[USERNAME]
        del os.environ[PASSWORD]
        del os.environ[INSTANCE_PROP]
        del os.environ[GTFS_SCHEDULE_SOURCE_CODE]
        del os.environ[STABLE_URL_PROP]
        del os.environ[CATALOG_PROP]
        del os.environ[GTFS_CATALOG_OF_SOURCES_CODE]

    @patch("helpers_cf.wbi_core")
    @patch("helpers_cf.wbi_login")
    def test_add_source_in_db_already_exists(self, mock_wbi_login, mock_wbi_core):
        os.environ[API_URL] = "api://url"
        os.environ[SPARQL_BIGDATA_URL] = "sparql://url"
        os.environ[USERNAME] = "usrname"
        os.environ[PASSWORD] = "pwd"
        os.environ[INSTANCE_PROP] = "instanceprop"
        os.environ[GTFS_SCHEDULE_SOURCE_CODE] = "gtfsschedprop"
        os.environ[STABLE_URL_PROP] = "gtfsschedprop"
        os.environ[CATALOG_PROP] = "gtfsschedprop"
        os.environ[GTFS_CATALOG_OF_SOURCES_CODE] = "gtfsschedprop"

        mock_wbi_core.ItemEngine.return_value.item_id = "Q1"

        source_name = "source name"
        stable_url = "stable://url"
        self.assertRaises(
            SourceAlreadyExistException, add_source_in_db, source_name, stable_url
        )

        del os.environ[API_URL]
        del os.environ[SPARQL_BIGDATA_URL]
        del os.environ[USERNAME]
        del os.environ[PASSWORD]
        del os.environ[INSTANCE_PROP]
        del os.environ[GTFS_SCHEDULE_SOURCE_CODE]
        del os.environ[STABLE_URL_PROP]
        del os.environ[CATALOG_PROP]
        del os.environ[GTFS_CATALOG_OF_SOURCES_CODE]


class DecodeMessageTestCase(unittest.TestCase):
    def test_decode_message(self):
        event = {
            "data": base64.b64encode(
                b"""{
                "source_name": "test_source_name",
                "dataset_url": "someurl",
                "source_entity_id": "someid"
            }"""
            )
        }
        message = decode_message(event)
        self.assertEqual(
            {
                "source_name": "test_source_name",
                "dataset_url": "someurl",
                "source_entity_id": "someid",
            },
            message,
        )

    def test_decode_message_falsy(self):
        event = {}
        message = decode_message(event)
        self.assertIsNone(message)


class AddDatasetTestCase(unittest.TestCase):
    @patch("helpers_cf.load_dataset")
    @patch("helpers_cf.process_md5")
    @patch("helpers_cf.download_dataset_as_zip")
    def test_add_dataset_to_source(
        self, mock_download_dataset_as_zip, mock_process_md5, mock_load_dataset
    ):
        os.environ[API_URL] = "api://url"
        os.environ[SPARQL_BIGDATA_URL] = "sparql://url"

        source_name = "source name"
        dataset_url = "dataset://url"
        dataset_entity_id = "Q1"
        data_type = "GTFS"

        mock_load_dataset.get_dataset_representations.return_value = {}
        # each process_ function being already tested, I'm not including a test case that goes through each and every of them.
        # unless it's deemed necessary.
        dataset_representations = add_dataset_to_source(
            source_name,
            dataset_url,
            dataset_entity_id,
            data_type,
            "someusername",
            "somepassword",
        )
        self.assertEqual([], dataset_representations)
