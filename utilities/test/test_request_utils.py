from unittest import TestCase, mock

from utilities.request_utils import (
    create_claim_string,
    create_regular_claim_string,
    create_wikibase_item_claim_string,
    create_geographical_claim_string,
    create_geographical_item,
    extract_dataset_version_codes,
    generate_api_csrf_token,
)
from utilities.constants import (
    STAGING_API_URL,
    STAGING_SPARQL_URL,
    VALUE,
    RESULTS,
    BINDINGS,
)


class TestClaimStringCreation(TestCase):
    def test_create_claim_string(self):
        test_property_id = "test_property_id"
        test_value = "test_value"
        test_rank = "test_rank"
        test_type = "test_type"
        test_datatype = "test_datatype"

        test_claim_string = """
        "test_property_id":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "test_property_id",
                    "datavalue": {
                        "value": test_value,
                        "type": "test_type"
                    },
                    "datatype": "test_datatype"
                },
                "type": "statement",
                "rank": "test_rank"
            }
        ]
        """

        under_test = create_claim_string(
            test_property_id, test_value, test_rank, test_type, test_datatype
        )
        self.assertEqual(under_test, test_claim_string)

    def test_create_regular_claim_string(self):
        test_property_id = "test_property_id"
        test_value = "test_value"
        test_rank = "test_rank"

        test_claim_string = """
        "test_property_id":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "test_property_id",
                    "datavalue": {
                        "value": "test_value",
                        "type": "string"
                    },
                    "datatype": "string"
                },
                "type": "statement",
                "rank": "test_rank"
            }
        ]
        """

        under_test = create_regular_claim_string(
            test_property_id, test_value, test_rank
        )
        self.assertEqual(under_test, test_claim_string)

    def test_create_wikibase_item_claim_string(self):
        test_property_id = "test_property_id"
        test_value = "test_value"
        test_rank = "test_rank"

        test_claim_string = """
        "test_property_id":[
            {
                "mainsnak": {
                    "snaktype": "value",
                    "property": "test_property_id",
                    "datavalue": {
                        "value": {
                "entity-type":"item", 
                "id":"test_value"
            },
                        "type": "wikibase-entityid"
                    },
                    "datatype": "wikibase-item"
                },
                "type": "statement",
                "rank": "test_rank"
            }
        ]
        """

        under_test = create_wikibase_item_claim_string(
            test_property_id, test_value, test_rank
        )
        self.assertEqual(under_test, test_claim_string)

    def test_create_geographical_claim_string(self):
        self.assertRaises(
            NotImplementedError, create_geographical_claim_string, None, None, None
        )

    def test_create_geographical_item(self):
        self.assertRaises(NotImplementedError, create_geographical_item, None, None)


class TestSparqlRequestUtils(TestCase):
    @mock.patch("utilities.request_utils.sparql_request")
    def test_extract_dataset_version_codes(self, mock_sparql_request):
        mock_sparql_request.return_value = {
            RESULTS: {
                BINDINGS: [
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q81-11337a5a-4b00-dfde-a946-a2efb7b9e30a"
                        }
                    },
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q78-a14a67ef-4ee9-a15d-b9de-d6be2e03d43d"
                        }
                    },
                ]
            }
        }

        test_entity_code = "test_entity_code"

        under_test = extract_dataset_version_codes(test_entity_code, STAGING_SPARQL_URL)
        self.assertEqual(under_test, {"Q81"})


class TestApiRequestUtils(TestCase):
    @mock.patch("utilities.request_utils.requests.post")
    @mock.patch("utilities.request_utils.requests.get")
    def test_generate_api_csrf_token(self, mock_get, mock_post):
        mock_post.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.side_effect = [
            {"query": {"tokens": {"logintoken": "test_login_token"}}},
            {"query": {"tokens": {"csrftoken": "test_csrf_token"}}},
        ]

        under_test = generate_api_csrf_token(STAGING_API_URL)
        self.assertEqual(under_test, "test_csrf_token")
