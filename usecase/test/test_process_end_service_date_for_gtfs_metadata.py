import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_service_date_for_gtfs_metadata import (
    process_end_service_date_for_gtfs_metadata,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY,
    DATE,
    SERVICE_ID,
    EXCEPTION_TYPE,
    END_DATE_MAP,
    CALENDAR_DATE_KEY,
    FEED_DATE_KEY,
)


class TestProcessEndServiceDateForGtfsMetadata(TestCase):
    def test_process_end_service_date_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(TypeError, process_end_service_date_for_gtfs_metadata, None)

    def test_process_end_service_date_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str

        self.assertRaises(
            TypeError,
            process_end_service_date_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    def test_process_end_service_date_with_dataset_with_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_service_date, "")

    def test_process_end_service_date_with_dataset_with_missing_fields(self):
        mock_feed_info = PropertyMock(return_value=pd.DataFrame({}))
        mock_calendar = PropertyMock(return_value=pd.DataFrame({}))
        mock_calendar_dates = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_service_date, "")

    def test_process_end_service_date_with_dataset_with_feed_info(self):
        mock_feed_info = PropertyMock(
            return_value=pd.DataFrame({END_DATE_MAP[FEED_DATE_KEY]: ["20201010"]})
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        self.assertEqual(mock_metadata.end_service_date, "2020-10-10")

    @mock.patch("usecase.process_service_date_for_gtfs_metadata.get_gtfs_dates_by_type")
    def test_process_end_service_date_with_dataset_with_empty_feed_info(
        self, mock_dates_by_type
    ):
        mock_feed_info = PropertyMock(
            return_value=pd.DataFrame({END_DATE_MAP[FEED_DATE_KEY]: []})
        )
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_DATE_MAP[CALENDAR_DATE_KEY]: ["20201010"],
                    MONDAY: [0],
                    TUESDAY: [0],
                    WEDNESDAY: [0],
                    THURSDAY: [0],
                    FRIDAY: [0],
                    SATURDAY: [1],
                    SUNDAY: [0],
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_calendar_dates = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_another_service_id"],
                    DATE: ["20201111"],
                    EXCEPTION_TYPE: [2],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
        )

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        mock_calendar.assert_called()
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_metadata.end_service_date, "2020-10-10")

    @mock.patch("usecase.process_service_date_for_gtfs_metadata.get_gtfs_dates_by_type")
    def test_process_end_service_date_with_dataset_with_none_feed_info(
        self, mock_dates_by_type
    ):
        mock_feed_info = PropertyMock(return_value=None)
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_DATE_MAP[CALENDAR_DATE_KEY]: ["20201010"],
                    MONDAY: [0],
                    TUESDAY: [0],
                    WEDNESDAY: [0],
                    THURSDAY: [0],
                    FRIDAY: [0],
                    SATURDAY: [1],
                    SUNDAY: [0],
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_calendar_dates = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_another_service_id"],
                    DATE: ["20201111"],
                    EXCEPTION_TYPE: [2],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
        )

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        mock_calendar.assert_called()
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_metadata.end_service_date, "2020-10-10")

    @mock.patch("usecase.process_service_date_for_gtfs_metadata.get_gtfs_dates_by_type")
    def test_process_end_service_date_with_dataset_with_none_feed_info_and_calendar(
        self, mock_dates_by_type
    ):
        mock_feed_info = PropertyMock(return_value=None)
        mock_calendar = PropertyMock(return_value=None)
        mock_calendar_dates = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_another_service_id"],
                    DATE: ["20201111"],
                    EXCEPTION_TYPE: [2],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
        )

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        mock_calendar.assert_called()
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_metadata.end_service_date, "2020-10-10")

    @mock.patch("usecase.process_service_date_for_gtfs_metadata.get_gtfs_dates_by_type")
    def test_process_end_service_date_with_dataset_with_none_feed_info_and_calendar_dates(
        self, mock_dates_by_type
    ):
        mock_feed_info = PropertyMock(return_value=None)
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_DATE_MAP[CALENDAR_DATE_KEY]: ["20201010"],
                    MONDAY: [0],
                    TUESDAY: [0],
                    WEDNESDAY: [0],
                    THURSDAY: [0],
                    FRIDAY: [0],
                    SATURDAY: [1],
                    SUNDAY: [0],
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_calendar_dates = PropertyMock(return_value=None)
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).feed_info = mock_feed_info
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
        )

        under_test = process_end_service_date_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_feed_info.assert_called()
        mock_calendar.assert_called()
        mock_calendar_dates.assert_called()
        self.assertEqual(mock_metadata.end_service_date, "2020-10-10")
