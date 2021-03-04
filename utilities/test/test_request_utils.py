from unittest import TestCase, mock

from utilities.request_utils import (
    extract_dataset_version_codes,
)
from utilities.constants import (
    STAGING_SPARQL_URL,
    VALUE,
    RESULTS,
    BINDINGS,
)


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
