import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_routes_count_by_type_for_gtfs_metadata import ProcessRoutesCountByTypeForGtfsMetadata


class ProcessRoutesCountByTypeForGtfsMetadataTest(TestCase):

    def test_process_routes_count_with_none_gtfs_representation_should_raise_exception(self):
        self.assertRaises(TypeError, ProcessRoutesCountByTypeForGtfsMetadata, None)

    def test_process_routes_count_with_invalid_gtfs_representation_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(TypeError, ProcessRoutesCountByTypeForGtfsMetadata, mock_gtfs_representation)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    def test_process_routes_count_with_valid_gtfs_representation_should_return_instance(self, mock_gtfs_representation):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = ProcessRoutesCountByTypeForGtfsMetadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, ProcessRoutesCountByTypeForGtfsMetadata)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_process_routes_count_execution_should_set_start_agencies_count_metadata(self, mock_gtfs_representation,
                                                                                     mock_dataset, mock_metadata):
        mock_routes = PropertyMock(return_value=pd.DataFrame({'route_type': [0, 2, 5, 0, 12, 1, 0, 0, 0]}))

        mock_dataset.__class__ = Feed
        type(mock_dataset).routes = mock_routes

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_representation.get_dataset.return_value = mock_dataset

        under_test = ProcessRoutesCountByTypeForGtfsMetadata(mock_gtfs_representation).execute()
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_gtfs_representation.get_dataset.assert_called_once()
        mock_routes.assert_called()
        self.assertEqual(mock_routes.call_count, 20)
        mock_gtfs_representation.set_metadata_routes_count_by_type.assert_called_with({'tram': '5',
                                                                                       'subway': '1',
                                                                                       'rail': '1',
                                                                                       'bus': '0',
                                                                                       'ferry': '0',
                                                                                       'cable_tram': '1',
                                                                                       'aerial_lift': '0',
                                                                                       'funicular': '0',
                                                                                       'trolley_bus': '0',
                                                                                       'monorail': '1'})
