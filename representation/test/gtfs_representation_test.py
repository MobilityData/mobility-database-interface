from unittest import TestCase, mock
from unittest.mock import MagicMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation


class GtfsRepresentationTest(TestCase):

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_with_none_entity_code_should_raise_exception(self, mock_dataset, mock_metadata):
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata
        self.assertRaises(TypeError, GtfsRepresentation, None, mock_dataset, mock_metadata)

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_with_invalid_entity_code_should_raise_exception(self, mock_dataset, mock_metadata):
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata
        self.assertRaises(TypeError, GtfsRepresentation, mock_dataset, mock_dataset, mock_metadata)

    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_with_none_dataset_should_raise_exception(self, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_metadata.__class__ = GtfsMetadata
        self.assertRaises(TypeError, GtfsRepresentation, mock_entity_code, None, mock_metadata)

    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_with_invalid_dataset_should_raise_exception(self, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_metadata.__class__ = GtfsMetadata
        self.assertRaises(TypeError, GtfsRepresentation, mock_entity_code, None, mock_metadata)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_gtfs_representation_with_none_metadata_should_raise_exception(self, mock_dataset):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        self.assertRaises(TypeError, GtfsRepresentation, mock_entity_code, mock_dataset, None)

    @mock.patch('gtfs_kit.feed.Feed')
    def test_gtfs_representation_with_invalid_metadata_should_raise_exception(self, mock_dataset):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        self.assertRaises(TypeError, GtfsRepresentation, mock_entity_code, mock_dataset, mock_dataset)

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_with_valid_parameters_should_return_instance(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        self.assertIsInstance(under_test, GtfsRepresentation)

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_get_dataset_should_return_dataset(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        self.assertEqual(under_test.get_dataset(), mock_dataset)

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_dataset_version_name_should_call_method(self,
                                                                                      mock_dataset,
                                                                                      mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_dataset_version_name("test_dataset_version_name")
        mock_metadata.set_dataset_version_name.assert_called_once()
        mock_metadata.set_dataset_version_name.assert_called_with("test_dataset_version_name")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_start_service_date_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_start_service_date("test_start_date")
        mock_metadata.set_start_service_date.assert_called_once()
        mock_metadata.set_start_service_date.assert_called_with("test_start_date")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_end_service_date_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_end_service_date("test_end_date")
        mock_metadata.set_end_service_date.assert_called_once()
        mock_metadata.set_end_service_date.assert_called_with("test_end_date")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_start_timestamp_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_start_timestamp("test_start_timestamp")
        mock_metadata.set_start_timestamp.assert_called_once()
        mock_metadata.set_start_timestamp.assert_called_with("test_start_timestamp")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_end_timestamp_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_end_timestamp("test_end_timestamp")
        mock_metadata.set_end_timestamp.assert_called_once()
        mock_metadata.set_end_timestamp.assert_called_with("test_end_timestamp")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_main_language_code_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_main_language_code("test_main_language_code")
        mock_metadata.set_main_language_code.assert_called_once()
        mock_metadata.set_main_language_code.assert_called_with("test_main_language_code")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_main_timezone_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_main_timezone("test_main_timezone")
        mock_metadata.set_main_timezone.assert_called_once()
        mock_metadata.set_main_timezone.assert_called_with("test_main_timezone")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_all_timezones_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_all_timezones(["test_all_timezones"])
        mock_metadata.set_all_timezones.assert_called_once()
        mock_metadata.set_all_timezones.assert_called_with(["test_all_timezones"])

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_bounding_box_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_bounding_box({"bounding_box": "bounding_box"})
        mock_metadata.set_bounding_box.assert_called_once()
        mock_metadata.set_bounding_box.assert_called_with({"bounding_box": "bounding_box"})

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_bounding_octagon_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_bounding_octagon({"bounding_octagon": "bounding_octagon"})
        mock_metadata.set_bounding_octagon.assert_called_once()
        mock_metadata.set_bounding_octagon.assert_called_with({"bounding_octagon": "bounding_octagon"})

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_agencies_count_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_agencies_count("test_agencies_count")
        mock_metadata.set_agencies_count.assert_called_once()
        mock_metadata.set_agencies_count.assert_called_with("test_agencies_count")

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_routes_count_by_type_should_call_method(self, mock_dataset,
                                                                                      mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_routes_count_by_type({"test_route_type": "test_count"})
        mock_metadata.set_routes_count_by_type.assert_called_once()
        mock_metadata.set_routes_count_by_type.assert_called_with({"test_route_type": "test_count"})

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_set_metadata_stops_count_by_type_should_call_method(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        under_test = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test.set_metadata_stops_count_by_type({"test_stop_type": "test_count"})
        mock_metadata.set_stops_count_by_type.assert_called_once()
        mock_metadata.set_stops_count_by_type.assert_called_with({"test_stop_type": "test_count"})

    @mock.patch('gtfs_kit.feed.Feed')
    @mock.patch('representation.gtfs_metadata.GtfsMetadata')
    def test_gtfs_representation_print_representation_should_return_none(self, mock_dataset, mock_metadata):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_dataset.__class__ = Feed
        mock_metadata.__class__ = GtfsMetadata

        gtfs_representation = GtfsRepresentation(mock_entity_code, mock_dataset, mock_metadata)
        under_test = gtfs_representation.print_representation()
        self.assertIsNone(under_test)
