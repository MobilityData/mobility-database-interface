import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_service_date_for_gtfs_metadata import (
    process_start_service_date_for_gtfs_metadata,
)


class TestProcessStartServiceDateForGtfsMetadata(TestCase):
    def test_process_start_service_date_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_start_service_date_for_gtfs_metadata, None)

    def test_process_start_service_date_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str

        self.assertRaises(
            TypeError,
            process_start_service_date_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_start_service_date_with_dataset_with_non_empty_feed_info_should_use_it(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_feed_info = PropertyMock(
            return_value=pd.DataFrame({"feed_start_date": ["20201010"]})
        )
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_start_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        self.assertEqual(mock_feed_info.call_count, 1)
        self.assertEqual(mock_metadata.start_service_date, "2020-10-10")

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_start_service_date_with_dataset_with_empty_feed_info_should_use_calendars(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_feed_info = PropertyMock(
            return_value=pd.DataFrame({"feed_start_date": []})
        )
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    "start_date": ["20201010"],
                    "monday": [0],
                    "tuesday": [0],
                    "wednesday": [0],
                    "thursday": [0],
                    "friday": [0],
                    "saturday": [1],
                    "sunday": [0],
                    "service_id": ["test_service_id"],
                }
            )
        )
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_start_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        self.assertEqual(mock_feed_info.call_count, 1)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 2)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)
        self.assertEqual(mock_metadata.start_service_date, "2020-10-10")

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_start_service_date_with_dataset_with_none_feed_info_should_use_calendars(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_feed_info = PropertyMock(return_value=None)
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    "start_date": ["20201010"],
                    "monday": [0],
                    "tuesday": [0],
                    "wednesday": [0],
                    "thursday": [0],
                    "friday": [0],
                    "saturday": [1],
                    "sunday": [0],
                    "service_id": ["test_service_id"],
                }
            )
        )
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_start_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        self.assertEqual(1, mock_feed_info.call_count)
        mock_calendar.assert_called()
        self.assertEqual(mock_calendar.call_count, 2)
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_calendar_dates.call_count, 1)
        self.assertEqual(mock_metadata.start_service_date, "2020-10-10")
