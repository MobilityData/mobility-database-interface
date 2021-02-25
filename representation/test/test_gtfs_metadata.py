from unittest import TestCase
from unittest.mock import MagicMock
from representation.gtfs_metadata import GtfsMetadata
from representation.dataset_infos import DatasetInfos


class TestGtfsMetadata(TestCase):
    def test_gtfs_metadata_with_none_dataset_infos_should_raise_exception(self):
        self.assertRaises(TypeError, GtfsMetadata, None)

    def test_gtfs_metadata_with_invalid_dataset_infos_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str

        self.assertRaises(TypeError, GtfsMetadata, mock_dataset_infos)

    def test_gtfs_metadata_with_valid_parameters_should_return_instance(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        under_test = GtfsMetadata(mock_dataset_infos)
        self.assertIsInstance(under_test, GtfsMetadata)

    def test_gtfs_metadata_to_string_special_method_should_return_metadata_string(self):
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

        test_md5_hash = "0123456789"
        test_source_name = "STM's GTFS Schedule source"
        test_download_date = "2021-01-10"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).md5_hash = test_md5_hash
        type(mock_dataset_infos).source_name = test_source_name
        type(mock_dataset_infos).download_date = test_download_date

        gtfs_metadata = GtfsMetadata(mock_dataset_infos)
        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)
