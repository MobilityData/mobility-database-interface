import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_all_timezones_for_gtfs_metadata import (
    process_all_timezones_for_gtfs_metadata,
)


class TestProcessMainTimezoneForGtfsMetadata(TestCase):
    def test_process_all_timezones_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_all_timezones_for_gtfs_metadata, None)

    def test_process_all_timezones_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError, process_all_timezones_for_gtfs_metadata, mock_gtfs_representation
        )

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_all_timezones_with_no_stop_timezone_should_add_main_timezone_to_list(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(return_value=pd.DataFrame())
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({"agency_timezone": ["America/Montreal"]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_all_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.all_timezones, ["America/Montreal"])

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_all_timezones_with_empty_stop_timezone_should_add_main_timezone_to_list(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(return_value=pd.DataFrame({"stop_timezone": []}))
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({"agency_timezone": ["America/Montreal"]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_all_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 2)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.all_timezones, ["America/Montreal"])

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_all_timezones_with_stop_timezones_should_add_these_to_list(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {"stop_timezone": ["America/Montreal", "America/Toronto"]}
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({"agency_timezone": ["America/Montreal"]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_all_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 2)
        mock_agency.assert_not_called()
        self.assertEqual(
            mock_metadata.all_timezones, ["America/Montreal", "America/Toronto"]
        )
