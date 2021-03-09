from unittest import TestCase, mock

from utilities.request_utils import (
    import_entity,
    extract_dataset_version_codes,
    extract_source_entity_codes,
)
from utilities.constants import (
    VALUE,
    RESULTS,
    BINDINGS,
)


class TestImportEntityRequestUtils(TestCase):
    @mock.patch("utilities.request_utils.wbi_core.ItemEngine")
    @mock.patch("utilities.request_utils.wbi_login")
    def test_import_entity_with_item_id(self, mock_login, mock_item_engine):
        test_username = "test_username "
        test_password = "test_password"
        test_properties = []
        test_label = "test_label"
        test_item_id = "test_item_id"

        mock_login.return_value = "test_login_instance"
        mock_item_engine.return_value.set_label.side_effect = None
        mock_item_engine.return_value.write.return_value = test_item_id

        under_test = import_entity(
            test_username, test_password, test_properties, test_label, test_item_id
        )
        self.assertEqual(under_test, test_item_id)

    @mock.patch("utilities.request_utils.wbi_core.ItemEngine")
    @mock.patch("utilities.request_utils.wbi_login")
    def test_import_entity_with_empty_item_id(self, mock_login, mock_item_engine):
        test_username = "test_username "
        test_password = "test_password"
        test_properties = []
        test_label = "test_label"
        test_item_id = ""

        mock_login.return_value = "test_login_instance"
        mock_item_engine.return_value.set_label.side_effect = None
        mock_item_engine.return_value.write.return_value = "test_new_entity"

        under_test = import_entity(
            test_username, test_password, test_properties, test_label, test_item_id
        )
        self.assertEqual(under_test, "test_new_entity")


class TestSparqlRequestUtils(TestCase):
    @mock.patch("utilities.request_utils.wbi_core.FunctionsEngine.execute_sparql_query")
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

        under_test = extract_dataset_version_codes(test_entity_code)
        self.assertEqual(under_test, {"Q81"})

    @mock.patch("utilities.request_utils.wbi_core.FunctionsEngine.execute_sparql_query")
    def test_extract_dataset_entity_codes(self, mock_sparql_request):
        mock_sparql_request.return_value = {
            RESULTS: {
                BINDINGS: [
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q80-8aece8db-417e-441b-0a5b-9c4a84c1efdf"
                        }
                    },
                    {
                        "a": {
                            VALUE: "http://wikibase.svc/entity/statement/Q82-d9dfdc30-47f0-f3d9-84a1-75b8d2fb0196"
                        }
                    },
                ]
            }
        }

        test_catalog_code = "test_catalog_code"

        under_test = extract_source_entity_codes(test_catalog_code)
        self.assertEqual(under_test, ["Q80", "Q82"])
