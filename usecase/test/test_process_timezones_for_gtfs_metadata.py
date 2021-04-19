import pandas as pd
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_timezones_for_gtfs_metadata import (
    process_timezones_for_gtfs_metadata,
    AGENCY_TIMEZONE,
    STOP_TIMEZONE,
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

    def test_process_timezones_with_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.main_timezone, "")
        self.assertEqual(mock_metadata.other_timezones, [])

    def test_process_timezones_with_missing_fields(self):
        mock_agency = PropertyMock(return_value=pd.DataFrame({}))
        mock_stops = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.main_timezone, "")
        self.assertEqual(mock_metadata.other_timezones, [])

    def test_process_timezones_with_missing_stop_timezones(self):
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE: [MONTREAL_TIMEZONE]})
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [])

    def test_process_timezones_with_missing_stop_timezones_fields(self):
        mock_stops = PropertyMock(return_value=pd.DataFrame())
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE: [MONTREAL_TIMEZONE]})
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [])

    def test_process_timezones_with_empty_stop_timezones(
        self,
    ):
        mock_stops = PropertyMock(return_value=pd.DataFrame({STOP_TIMEZONE: []}))
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE: [MONTREAL_TIMEZONE]})
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [])

    def test_process_timezones_with_missing_agency(self):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_TIMEZONE: [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]}
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        self.assertEqual(mock_metadata.main_timezone, "")
        self.assertEqual(
            mock_metadata.other_timezones, [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]
        )

    def test_process_timezones_with_missing_agency_fields(
        self,
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_TIMEZONE: [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]}
            )
        )
        mock_agency = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, "")
        self.assertEqual(
            mock_metadata.other_timezones, [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]
        )

    def test_process_timezones_with_empty_agency(
        self,
    ):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_TIMEZONE: [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]}
            )
        )
        mock_agency = PropertyMock(return_value=pd.DataFrame({AGENCY_TIMEZONE: []}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, "")
        self.assertEqual(
            mock_metadata.other_timezones, [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]
        )

    def test_process_timezones(self):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_TIMEZONE: [MONTREAL_TIMEZONE, TORONTO_TIMEZONE]}
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame({AGENCY_TIMEZONE: [MONTREAL_TIMEZONE]})
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_timezones_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_stops.assert_called()
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_timezone, MONTREAL_TIMEZONE)
        self.assertEqual(mock_metadata.other_timezones, [TORONTO_TIMEZONE])
