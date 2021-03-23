import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
    AGENCY_TIMEZONE_KEY,
    STOP_TIMEZONE_KEY,
)

MONTREAL_TIMEZONE = "America/Montreal"
TORONTO_TIMEZONE = "America/Toronto"


class TestProcessTimezonesForGtfsMetadata(TestCase):
    def test_process_timezones_with_none_gtfs_representation(
        self,
    ):
        self.assertRaises(TypeError, process_timezones_for_gtfs_metadata, None)

    def test_process_timezones_with_invalid_gtfs_representation(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError, process_timezones_for_gtfs_metadata, mock_gtfs_representation
        )

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_timezones_with_no_stop_timezones(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(return_value=pd.DataFrame())
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE_KEY: [MONTREAL_TIMEZONE]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 1)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [])

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_timezones_with_empty_stop_timezones(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(return_value=pd.DataFrame({STOP_TIMEZONE_KEY: []}))
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE_KEY: [MONTREAL_TIMEZONE]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 2)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [])

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_timezones_with_stop_timezones(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_TIMEZONE_KEY: [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]}
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE_KEY: [MONTREAL_TIMEZONE]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_stops.call_count, 2)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [TORONTO_TIMEZONE])
