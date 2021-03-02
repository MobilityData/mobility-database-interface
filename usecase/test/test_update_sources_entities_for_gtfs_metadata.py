from unittest import TestCase, mock
from unittest.mock import MagicMock

from representation.dataset_infos import DatasetInfos
from usecase.update_source_entities_for_gtfs_metadata import (
    create_data,
    update_source_entities_for_gtfs_metadata,
)
from utilities.constants import STAGING_API_URL, STAGING_SPARQL_URL


class TestDataCreationForSourceEntitiesUpdate(TestCase):
    def test_create_data_with_valid_metadata_should_return_data(self):

        test_version_code = "test_version_code"

        test_data = """{
            "claims":{
                
        "P64":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "P64",
                    "datavalue": {
                        "value": {
                "entity-type":"item", 
                "id":"test_version_code"
            },
                        "type": "wikibase-entityid"
                    },
                    "datatype": "wikibase-item"
                },
                "type": "statement",
                "rank": "normal"
            }
        ]
        
            }
        }"""

        under_test = create_data(test_version_code)
        self.assertEqual(under_test, test_data)


class TestUpdateSourceEntities(TestCase):
    def test_update_source_entities_with_invalid_api_url_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]

        test_api_url = "test_api_url"

        self.assertRaises(
            TypeError,
            update_source_entities_for_gtfs_metadata,
            mock_datasets_infos,
            test_api_url,
            STAGING_SPARQL_URL,
        )

    def test_update_source_entities_with_invalid_sparql_api_should_raise_exception(
        self,
    ):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]

        test_sparql_api = "test_sparql_api"

        self.assertRaises(
            TypeError,
            update_source_entities_for_gtfs_metadata,
            mock_datasets_infos,
            STAGING_API_URL,
            test_sparql_api,
        )

    def test_create_dataset_entity_with_invalid_datasets_infos_should_raise_exception(
        self,
    ):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError,
            update_source_entities_for_gtfs_metadata,
            mock_datasets_infos,
            STAGING_API_URL,
            STAGING_SPARQL_URL,
        )

        mock_datasets_infos = MagicMock()
        self.assertRaises(
            TypeError,
            update_source_entities_for_gtfs_metadata,
            str(mock_datasets_infos),
            STAGING_API_URL,
            STAGING_SPARQL_URL,
        )

    @mock.patch(
        "usecase.update_source_entities_for_gtfs_metadata.extract_dataset_version_codes"
    )
    @mock.patch(
        "usecase.update_source_entities_for_gtfs_metadata.generate_api_csrf_token"
    )
    @mock.patch("usecase.update_source_entities_for_gtfs_metadata.requests.post")
    def test_update_source_entities_with_valid_parameter_should_post_request_and_return_representation(
        self, mock_api_request, mock_api_token, mock_version_codes
    ):
        mock_api_request.return_value.raise_for_status.return_value = None
        mock_api_token.return_value = "test_token"
        mock_version_codes.return_value = {"test_version_codes"}

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).previous_versions = set()
        mock_datasets_infos = [mock_dataset_infos]

        under_test = update_source_entities_for_gtfs_metadata(
            mock_datasets_infos, STAGING_API_URL, STAGING_SPARQL_URL
        )
        self.assertEqual(under_test, mock_datasets_infos)
