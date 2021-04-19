import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_timestamp_for_gtfs_metadata import (
    process_end_timestamp_for_gtfs_metadata,
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
    TRIP_ID,
    AGENCY_TIMEZONE,
    END_TIMESTAMP_MAP,
    CALENDAR_DATE_KEY,
    STOP_TIME_KEY,
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

    def test_process_end_timestamp_execution_missing_both_calendar_files(self):
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_calendar_fields(self):
        mock_calendar = PropertyMock(return_value=pd.DataFrame({}))
        mock_calendar_dates = PropertyMock(return_value=pd.DataFrame({}))
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_stop_times_file(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_stop_times_fields(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(return_value=pd.DataFrame({}))
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_trips_file(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_trips_fields(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(return_value=pd.DataFrame({}))
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_agency_file(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    def test_process_end_timestamp_execution_missing_agency_fields(self):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "")

    @mock.patch("usecase.process_timestamp_for_gtfs_metadata.get_gtfs_dates_by_type")
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_timezone_utc_offset"
    )
    @mock.patch(
        "usecase.process_timestamp_for_gtfs_metadata.get_gtfs_stop_times_for_date"
    )
    def test_process_end_timestamp_execution_with_no_calendar_dates(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {TRIP_ID: ["test_trip_id"], END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
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
    def test_process_end_timestamp_execution_with_no_calendar(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {TRIP_ID: ["test_trip_id"], END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
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
    def test_process_end_timestamp_execution_should_set_start_timestamp_metadata(
        self, mock_stop_times_for_date, mock_utc_offset, mock_dates_by_type
    ):
        mock_calendar = PropertyMock(
            return_value=pd.DataFrame(
                {
                    END_TIMESTAMP_MAP[CALENDAR_DATE_KEY]: ["20201010"],
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
        mock_stop_times = PropertyMock(
            return_value=pd.DataFrame(
                {
                    TRIP_ID: ["test_trip_id"],
                    END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["test_stop_time"],
                }
            )
        )
        mock_trips = PropertyMock(
            return_value=pd.DataFrame(
                {
                    SERVICE_ID: ["test_service_id"],
                }
            )
        )
        mock_agency = PropertyMock(
            return_value=pd.DataFrame(
                {
                    AGENCY_TIMEZONE: ["test_agency_timezone"],
                }
            )
        )
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).calendar = mock_calendar
        type(mock_dataset).calendar_dates = mock_calendar_dates
        type(mock_dataset).stop_times = mock_stop_times
        type(mock_dataset).trips = mock_trips
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_stop_times_for_date.return_value = pd.DataFrame(
            {TRIP_ID: ["test_trip_id"], END_TIMESTAMP_MAP[STOP_TIME_KEY]: ["05:00:00"]}
        )

        mock_dates_by_type.return_value = pd.DataFrame(
            {SERVICE_ID: ["test_service_id"], DATE: ["20201010"]}
        )

        mock_utc_offset.return_value = "-05:00"

        under_test = process_end_timestamp_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.end_timestamp, "2020-10-10T05:00:00-05:00")
