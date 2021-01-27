import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_main_timezone_for_gtfs_metadata import ProcessMainTimezoneForGtfsMetadata


class ProcessMainTimezoneForGtfsMetadataTest(TestCase):

    def test_process_main_timezone_with_none_gtfs_representation_should_raise_exception(self):
        self.assertRaises(TypeError, ProcessMainTimezoneForGtfsMetadata, None)

    def test_process_main_timezone_with_invalid_gtfs_representation_should_raise_exception(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(TypeError, ProcessMainTimezoneForGtfsMetadata, mock_gtfs_representation)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    def test_process_main_timezone_with_valid_gtfs_representation_should_return_instance(self,
                                                                                         mock_gtfs_representation):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = ProcessMainTimezoneForGtfsMetadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, ProcessMainTimezoneForGtfsMetadata)

    @mock.patch('representation.gtfs_representation.GtfsRepresentation')
    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_process_main_timezone_with_gtfs_dataset_should_add_main_timezone_to_gtfs_metadata(self,
                                                                                               mock_gtfs_representation,
                                                                                               mock_dataset,
                                                                                               mock_metadata):
        mock_agency = PropertyMock(return_value=pd.DataFrame({'agency_timezone': ['America/Montreal']}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        mock_gtfs_representation.get_dataset.return_value = mock_dataset

        under_test = ProcessMainTimezoneForGtfsMetadata(mock_gtfs_representation).execute()
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_gtfs_representation.get_dataset.assert_called_once()
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        mock_gtfs_representation.set_metadata_main_timezone.assert_called_with('America/Montreal')
