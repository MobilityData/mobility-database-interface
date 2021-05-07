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
            "Main timezone: None\n"
            "Other timezones: None\n"
            "Country codes: None\n"
            "Main language code: None\n"
            "Start service date: None\n"
            "End service date: None\n"
            "Start timestamp: None\n"
            "End timestamp: None\n"
            "Bounding box: None\n"
            "Bounding octagon: None\n"
            "Agencies count: None\n"
            "Routes count by type: None\n"
            "Stops count by type: None\n"
            "Stable url: None\n"
            "SHA-1 hash: 0123456789"
        )

        test_sha1_hash = "0123456789"
        test_source_name = "STM's GTFS Schedule source"
        test_download_date = "2021-01-10"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).sha1_hash = test_sha1_hash
        type(mock_dataset_infos).source_name = test_source_name
        type(mock_dataset_infos).download_date = test_download_date

        gtfs_metadata = GtfsMetadata(mock_dataset_infos)
        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)

        test_metadata_string = (
            "Dataset version name: 2021-01-10's STM's GTFS Schedule dataset #012345\n"
            "Main timezone: test_main_timezone\n"
            "Other timezones: ['test_other_timezones']\n"
            "Country codes: ['test_country_codes']\n"
            "Main language code: test_main_language_code\n"
            "Start service date: test_start_service_date\n"
            "End service date: test_end_service_date\n"
            "Start timestamp: test_start_timestamp\n"
            "End timestamp: test_end_timestamp\n"
            "Bounding box: {'test_bounding_box_key': 'test_bounding_box_value'}\n"
            "Bounding octagon: {'test_bounding_octagon_key': 'test_bounding_octagon_value'}\n"
            "Agencies count: 1\n"
            "Routes count by type: {'test_routes_type': 1}\n"
            "Stops count by type: {'test_stops_type': 1}\n"
            "Stable url: test_stable_url\n"
            "SHA-1 hash: 0123456789"
        )

        test_sha1_hash = "0123456789"
        test_source_name = "STM's GTFS Schedule source"
        test_download_date = "2021-01-10"
        test_main_timezone = "test_main_timezone"
        test_other_timezones = ["test_other_timezones"]
        test_country_codes = ["test_country_codes"]
        test_main_language_code = "test_main_language_code"
        test_start_service_date = "test_start_service_date"
        test_end_service_date = "test_end_service_date"
        test_start_timestamp = "test_start_timestamp"
        test_end_timestamp = "test_end_timestamp"
        test_bounding_box = {"test_bounding_box_key": "test_bounding_box_value"}
        test_bounding_octagon = {
            "test_bounding_octagon_key": "test_bounding_octagon_value"
        }
        test_agencies_count = 1
        test_routes_count_by_type = {"test_routes_type": 1}
        test_stops_count_by_type = {"test_stops_type": 1}
        test_stable_url = "test_stable_url"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).sha1_hash = test_sha1_hash
        type(mock_dataset_infos).source_name = test_source_name
        type(mock_dataset_infos).download_date = test_download_date

        gtfs_metadata = GtfsMetadata(mock_dataset_infos)
        gtfs_metadata.main_timezone = test_main_timezone
        gtfs_metadata.other_timezones = test_other_timezones
        gtfs_metadata.country_codes = test_country_codes
        gtfs_metadata.main_language_code = test_main_language_code
        gtfs_metadata.start_service_date = test_start_service_date
        gtfs_metadata.end_service_date = test_end_service_date
        gtfs_metadata.start_timestamp = test_start_timestamp
        gtfs_metadata.end_timestamp = test_end_timestamp
        gtfs_metadata.bounding_box = test_bounding_box
        gtfs_metadata.bounding_octagon = test_bounding_octagon
        gtfs_metadata.agencies_count = test_agencies_count
        gtfs_metadata.routes_count_by_type = test_routes_count_by_type
        gtfs_metadata.stops_count_by_type = test_stops_count_by_type
        gtfs_metadata.stable_url = test_stable_url

        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)
