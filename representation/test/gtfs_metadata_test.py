from unittest import TestCase
from unittest.mock import MagicMock
from representation.gtfs_metadata import GtfsMetadata


class GtfsMetadataTest(TestCase):

    def test_gtfs_metadata_with_none_md5_hash_should_raise_exception(self):
        self.assertRaises(TypeError, GtfsMetadata, None)

    def test_gtfs_metadata_with_invalid_md5_hash_string_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = int
        self.assertRaises(TypeError, GtfsMetadata, mock_md5_hash)

    def test_gtfs_metadata_with_valid_md5_hash_string_should_return_instance(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertIsInstance(under_test, GtfsMetadata)

    def test_gtfs_metadata_get_start_service_date_should_return_start_service_date(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_start_service_date(), "")

    def test_gtfs_metadata_set_start_service_date_should_set_start_service_date(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_start_service_date(), "")

        under_test.set_start_service_date("test_start_date")
        self.assertEqual(under_test.get_start_service_date(), "test_start_date")

    def test_gtfs_metadata_get_end_service_date_should_return_end_service_date(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_end_service_date(), "")

    def test_gtfs_metadata_set_end_service_date_should_set_end_service_date(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_end_service_date(), "")

        under_test.set_end_service_date("test_end_date")
        self.assertEqual(under_test.get_end_service_date(), "test_end_date")

    def test_gtfs_metadata_get_start_timestamp_should_return_start_timestamp(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_start_timestamp(), "")

    def test_gtfs_metadata_set_start_timestamp_should_set_start_timestamp(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_start_timestamp(), "")

        under_test.set_start_timestamp("test_start_timestamp")
        self.assertEqual(under_test.get_start_timestamp(), "test_start_timestamp")

    def test_gtfs_metadata_get_end_timestamp_should_return_end_timestamp(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_start_timestamp(), "")

    def test_gtfs_metadata_set_end_timestamp_should_set_end_timestamp(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_end_timestamp(), "")

        under_test.set_end_timestamp("test_end_timestamp")
        self.assertEqual(under_test.get_end_timestamp(), "test_end_timestamp")

    def test_gtfs_metadata_get_main_timezone_should_return_main_timezone(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_main_timezone(), "")

    def test_gtfs_metadata_set_main_timezone_should_set_main_timezone(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_main_timezone(), "")

        under_test.set_main_timezone("test_main_timezone")
        self.assertEqual(under_test.get_main_timezone(), "test_main_timezone")

    def test_gtfs_metadata_get_all_timezones_should_return_all_timezones(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_all_timezones(), [])

    def test_gtfs_metadata_set_main_timezone_should_set_main_timezone(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertEqual(under_test.get_all_timezones(), [])

        under_test.set_main_timezone(["test_all_timezones"])
        self.assertEqual(under_test.get_main_timezone(), ["test_all_timezones"])

    def test_gtfs_metadata_to_string_special_method_should_return_metadata_string(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str
        mock_md5_hash.__str__.return_value = 'test_md5_hash'

        test_metadata_string = "Main timezone: \n" \
                               "All timezones: \n" \
                               "Country code: \n" \
                               "Sub country code: \n" \
                               "Language code: \n" \
                               "Start service date: \n" \
                               "End service date: \n" \
                               "Start timestamp: \n" \
                               "End timestamp: \n" \
                               "Bounding box: \n" \
                               "Stable url: \n" \
                               "MD5 hash: test_md5_hash"

        gtfs_metadata = GtfsMetadata(str(mock_md5_hash))
        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)
