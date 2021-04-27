import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_routes_count_by_type_for_gtfs_metadata import (
    process_routes_count_by_type_for_gtfs_metadata,
    ROUTE_TYPE,
    TRAM_CODE,
    SUBWAY_CODE,
    RAIL_CODE,
    BUS_CODE,
    FERRY_CODE,
    CABLE_TRAM_CODE,
    AERIAL_LIFT_CODE,
    FUNICULAR_CODE,
    TROLLEY_BUS_CODE,
    MONORAIL_CODE,
)


class TestProcessRoutesCountByTypeForGtfsMetadata(TestCase):
    def test_process_routes_count_with_none_gtfs_representation_should_raise_exception(
        self,
    ):
        self.assertRaises(
            TypeError, process_routes_count_by_type_for_gtfs_metadata, None
        )

    def test_process_routes_count_with_invalid_gtfs_representation_should_raise_exception(
        self,
    ):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError,
            process_routes_count_by_type_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    @mock.patch("usecase.process_routes_count_by_type_for_gtfs_metadata.os.environ")
    def test_process_routes_count_with_valid_gtfs_representation_should_return_instance(
        self, mock_env
    ):
        test_env = {
            TRAM_CODE: "test_tram_code",
            SUBWAY_CODE: "test_subway_code",
            RAIL_CODE: "test_rail_code",
            BUS_CODE: "test_bus_code",
            FERRY_CODE: "test_ferry_code",
            CABLE_TRAM_CODE: "test_cable_tram_code",
            AERIAL_LIFT_CODE: "test_aerial_lift_code",
            FUNICULAR_CODE: "test_funicular_code",
            TROLLEY_BUS_CODE: "test_trolley_bus_code",
            MONORAIL_CODE: "test_monorail_code",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = process_routes_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)

    @mock.patch("usecase.process_routes_count_by_type_for_gtfs_metadata.os.environ")
    def test_process_routes_count_execution_should_set_start_agencies_count_metadata(
        self, mock_env
    ):
        test_env = {
            TRAM_CODE: "test_tram_code",
            SUBWAY_CODE: "test_subway_code",
            RAIL_CODE: "test_rail_code",
            BUS_CODE: "test_bus_code",
            FERRY_CODE: "test_ferry_code",
            CABLE_TRAM_CODE: "test_cable_tram_code",
            AERIAL_LIFT_CODE: "test_aerial_lift_code",
            FUNICULAR_CODE: "test_funicular_code",
            TROLLEY_BUS_CODE: "test_trolley_bus_code",
            MONORAIL_CODE: "test_monorail_code",
        }
        mock_env.__getitem__.side_effect = test_env.__getitem__

        mock_routes = PropertyMock(
            return_value=pd.DataFrame({ROUTE_TYPE: [0, 2, 5, 0, 12, 1, 0, 0, 0]})
        )

        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).routes = mock_routes

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_routes_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_routes.assert_called()
        self.assertEqual(mock_routes.call_count, 20)
        self.assertEqual(
            mock_metadata.routes_count_by_type,
            {
                "test_tram_code": 5,
                "test_subway_code": 1,
                "test_rail_code": 1,
                "test_bus_code": 0,
                "test_ferry_code": 0,
                "test_cable_tram_code": 1,
                "test_aerial_lift_code": 0,
                "test_funicular_code": 0,
                "test_trolley_bus_code": 0,
                "test_monorail_code": 1,
            },
        )
