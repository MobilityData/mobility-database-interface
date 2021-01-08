from representation.gtfs_representation import GtfsRepresentation
from request_manager.api_request_manager import ApiRequestManager


class DatasetEntityCreationForGtfsMetadata:

    def __init__(self, gtfs_representation, api_request_manager):
        """Constructor for ``DatasetEntityCreationForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        :param api_request_manager: API request manager used to process API requests.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
            if api_request_manager is None or not isinstance(api_request_manager, ApiRequestManager):
                raise TypeError("API request manager must be a valid ApiRequestManager.")
            self.api_request_manager = api_request_manager
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``DatasetEntityCreationForGtfsMetadata`` use case.
        :return: The representation of the GTFS dataset post-execution.
        """
        data = {
            "labels": {
                "en": {
                    "language": "en",
                    "value": "test-dataset"}
            },
            "claims": {
                "P20": [{
                    "mainsnak": {
                        "snaktype": "value",
                        "property": "P20",
                        "datavalue": {
                            "value": {
                                "entity-type": "item",
                                "numeric-id": 29,
                                "id": "Q29"
                            },
                            "type": "wikibase-entityid"
                        },
                        "datatype": "wikibase-item"
                    },
                    "type": "statement",
                    "rank": "normal"
                }]
            }
        }

        params = {
            "action": "wbeditentity",
            "new": "item",
            "data": "%s" % data
        }
        api_response = self.api_request_manager.execute_get(params)

        return self.gtfs_representation
