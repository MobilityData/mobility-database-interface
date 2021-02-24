from unittest import TestCase
from unittest.mock import MagicMock
from representation.gtfs_metadata import GtfsMetadata


class GtfsMetadataTest(TestCase):
    def test_gtfs_metadata_with_none_md5_hash_should_raise_exception(self):
        mock_source_name = MagicMock()
        mock_source_name.__class__ = str

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str

        self.assertRaises(
            TypeError, GtfsMetadata, None, mock_source_name, mock_download_date
        )

    def test_gtfs_metadata_with_invalid_md5_hash_string_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = int

        mock_source_name = MagicMock()
        mock_source_name.__class__ = str

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str

        self.assertRaises(
            TypeError, GtfsMetadata, mock_md5_hash, mock_source_name, mock_download_date
        )

    def test_gtfs_metadata_with_none_source_name_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str

        self.assertRaises(
            TypeError, GtfsMetadata, mock_md5_hash, None, mock_download_date
        )

    def test_gtfs_metadata_with_invalid_source_name_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        mock_source_name = MagicMock()
        mock_source_name.__class__ = int

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str

        self.assertRaises(
            TypeError, GtfsMetadata, mock_md5_hash, mock_source_name, mock_download_date
        )

    def test_gtfs_metadata_with_none_download_date_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        mock_source_name = MagicMock()
        mock_source_name.__class__ = str

        self.assertRaises(
            TypeError, GtfsMetadata, mock_md5_hash, mock_source_name, None
        )

    def test_gtfs_metadata_with_invalid_download_date_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        mock_source_name = MagicMock()
        mock_source_name.__class__ = str

        mock_download_date = MagicMock()
        mock_download_date.__class__ = int

        self.assertRaises(
            TypeError, GtfsMetadata, mock_md5_hash, mock_source_name, mock_download_date
        )

    def test_gtfs_metadata_with_valid_parameters_should_return_instance(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        mock_source_name = MagicMock()
        mock_source_name.__class__ = str

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash, mock_source_name, mock_download_date)
        self.assertIsInstance(under_test, GtfsMetadata)

    def test_gtfs_metadata_to_string_special_method_should_return_metadata_string(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str
        mock_md5_hash.__str__.return_value = "0123456789"

        mock_source_name = MagicMock()
        mock_source_name.__class__ = str
        mock_source_name.__str__.return_value = "STM's GTFS Schedule source"

        mock_download_date = MagicMock()
        mock_download_date.__class__ = str
        mock_download_date.__str__.return_value = "2021-01-10"

        test_metadata_string = (
            "Dataset version name: 2021-01-10's STM's GTFS Schedule dataset #012345\n"
            "Main timezone: \n"
            "All timezones: \n"
            "Country code: \n"
            "Sub country code: \n"
            "Main language code: \n"
            "Start service date: \n"
            "End service date: \n"
            "Start timestamp: \n"
            "End timestamp: \n"
            "Bounding box: {}\n"
            "Bounding octagon: {}\n"
            "Agencies count: 0\n"
            "Routes count by type: {}\n"
            "Stops count by type: {}\n"
            "Stable url: \n"
            "MD5 hash: 0123456789"
        )

        gtfs_metadata = GtfsMetadata(
            str(mock_md5_hash), str(mock_source_name), str(mock_download_date)
        )
        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)
