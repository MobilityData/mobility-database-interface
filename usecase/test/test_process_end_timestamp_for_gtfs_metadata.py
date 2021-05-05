import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_timestamp_for_gtfs_metadata import (
    process_end_timestamp_for_gtfs_metadata,
)


class TestProcessEndTimestampForGtfsMetadata(TestCase):
    def test_process_end_timestamp_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_end_timestamp_for_gtfs_metadata, None)

    def test_process_end_timestamp_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError, process_end_timestamp_for_gtfs_metadata, mock_gtfs_representation
        )

    @mock.patch("usecase.process_timestamp_for_gtfs_metadata.get_gtfs_dates_by_type")
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_timezone_utc_offset"
    )
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_stop_times_for_date"
    )
    def test_process_end_timestamp_execution_should_set_start_timestamp_metadata(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {"trip_id": ["test_trip_id"], "departure_time": ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {"service_id": ["test_service_id"], "date": ["20201010"]}
        )

        mock_utc_offset.return_value = "-05:00"

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "2020-10-10T05:00:00-05:00")

    @mock.patch("usecase.process_timestamp_for_gtfs_metadata.get_gtfs_dates_by_type")
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_timezone_utc_offset"
    )
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_stop_times_for_date"
    )
    def test_process_end_timestamp_execution_with_empty_dates_by_type(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {"trip_id": ["test_trip_id"], "departure_time": ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame({"service_id": [], "date": []})

        mock_utc_offset.return_value = "-05:00"

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_metadata.end_timestamp.assert_not_called()

    @mock.patch("usecase.process_timestamp_for_gtfs_metadata.get_gtfs_dates_by_type")
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_timezone_utc_offset"
    )
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_stop_times_for_date"
    )
    def test_process_end_timestamp_execution_with_empty_stop_times_for_date(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {"trip_id": [], "departure_time": []}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {"service_id": ["test_service_id"], "date": ["20201010"]}
        )

        mock_utc_offset.return_value = "-05:00"

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_metadata.end_timestamp.assert_not_called()

    @mock.patch("usecase.process_timestamp_for_gtfs_metadata.get_gtfs_dates_by_type")
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_timezone_utc_offset"
    )
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_stop_times_for_date"
    )
    def test_process_end_timestamp_execution_with_empty_timezone_utc_offset(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {"trip_id": ["test_trip_id"], "departure_time": ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {"service_id": ["test_service_id"], "date": ["20201010"]}
        )

        mock_utc_offset.return_value = ""

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_metadata.end_timestamp.assert_not_called()
