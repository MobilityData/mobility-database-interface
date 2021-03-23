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

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_process_routes_count_with_valid_gtfs_representation_should_return_instance(
        self, mock_gtfs_representation
    ):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = process_routes_count_by_type_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_routes_count_execution_should_set_start_agencies_count_metadata(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_routes = PropertyMock(
            return_value=pd.DataFrame({ROUTE_TYPE: [0, 2, 5, 0, 12, 1, 0, 0, 0]})
        )

        mock_dataset.__class__ = Feed
        type(mock_dataset).routes = mock_routes

        mock_metadata.__class__ = GtfsMetadata
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
                TRAM_CODE: 5,
                SUBWAY_CODE: 1,
                RAIL_CODE: 1,
                BUS_CODE: 0,
                FERRY_CODE: 0,
                CABLE_TRAM_CODE: 1,
                AERIAL_LIFT_CODE: 0,
                FUNICULAR_CODE: 0,
                TROLLEY_BUS_CODE: 0,
                MONORAIL_CODE: 1,
            },
        )
