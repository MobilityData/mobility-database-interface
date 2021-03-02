from unittest import TestCase, mock
from unittest.mock import Mock, MagicMock

from representation.gtfs_representation import GtfsRepresentation
from representation.gtfs_metadata import GtfsMetadata
from usecase.create_dataset_entity_for_gtfs_metadata import (
    create_data,
    create_dataset_entity_for_gtfs_metadata,
)
from utilities.constants import STAGING_API_URL


class TestDataCreation(TestCase):
    def test_create_data_with_valid_metadata_should_return_data(self):
        mock_metadata = MagicMock()

        type(mock_metadata).dataset_version_name = "test_version_name"
        type(mock_metadata).source_entity_code = "test_entity_code"
        type(mock_metadata).main_timezone = "test_main_timezone"
        type(mock_metadata).main_language_code = "test_main_language"
        type(mock_metadata).start_service_date = "test_start_service_date"
        type(mock_metadata).end_service_date = "test_end_service_date"
        type(mock_metadata).start_timestamp = "test_start_timestamp"
        type(mock_metadata).end_timestamp = "test_end_timestamp"
        type(mock_metadata).md5_hash = "test_md5_hash"

        test_data = """{
            "labels": {
                "en": {
                    "language": "en",
                    "value": "test_version_name"
                }
            },
            "claims": {
                
        "P20":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P20",
                    "datavalue": {
                        "value": {
                "entity-type":"item", 
                "id":"Q29"
            },
                        "type": "wikibase-entityid"
                    },
                    "datatype": "wikibase-item"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P48":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P48",
                    "datavalue": {
                        "value": {
                "entity-type":"item", 
                "id":"test_entity_code"
            },
                        "type": "wikibase-entityid"
                    },
                    "datatype": "wikibase-item"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P49":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P49",
                    "datavalue": {
                        "value": "test_main_timezone",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "preferred"
            }
        ]
        ,
                
        "P54":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P54",
                    "datavalue": {
                        "value": "test_main_language",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "preferred"
            }
        ]
        ,
                
        "P52":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P52",
                    "datavalue": {
                        "value": "test_start_service_date",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P53":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P53",
                    "datavalue": {
                        "value": "test_end_service_date",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P66":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P66",
                    "datavalue": {
                        "value": "test_start_timestamp",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P67":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P67",
                    "datavalue": {
                        "value": "test_end_timestamp",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        ,
                
        "P61":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P61",
                    "datavalue": {
                        "value": "test_md5_hash",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        
            }
        }"""

        under_test = create_data(mock_metadata)
        self.assertEqual(under_test, test_data)


class TestCreateDatasetEntity(TestCase):
    def test_create_dataset_entity_with_invalid_api_url_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation

        test_api_url = "test_api_url"

        self.assertRaises(
            TypeError,
            create_dataset_entity_for_gtfs_metadata,
            mock_gtfs_representation,
            test_api_url,
        )

    def test_create_dataset_entity_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str

        self.assertRaises(
            TypeError,
            create_dataset_entity_for_gtfs_metadata,
            mock_gtfs_representation,
            STAGING_API_URL,
        )

    @mock.patch(
        "usecase.create_dataset_entity_for_gtfs_metadata.generate_api_csrf_token"
    )
    @mock.patch("usecase.create_dataset_entity_for_gtfs_metadata.requests.post")
    def test_create_dataset_entity_with_valid_parameter_should_post_request_and_return_representation(
        self, mock_api_request, mock_api_token
    ):
        mock_api_request.return_value.raise_for_status.return_value = None
        mock_api_token.return_value = "test_token"

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_metadata = MagicMock()
        mock_gtfs_metadata.__class__ = GtfsMetadata
        type(mock_gtfs_representation).metadata = mock_gtfs_metadata

        under_test = create_dataset_entity_for_gtfs_metadata(
            mock_gtfs_representation, STAGING_API_URL
        )
        self.assertEqual(under_test, mock_gtfs_representation)
