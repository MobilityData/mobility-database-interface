import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_routes_count_by_type_for_gtfs_metadata import (
    process_routes_count_by_type_for_gtfs_metadata,
    ROUTE_TYPE,
    TRAM_KEY,
    SUBWAY_KEY,
    RAIL_KEY,
    BUS_KEY,
    FERRY_KEY,
    CABLE_TRAM_KEY,
    AERIAL_LIFT_KEY,
    FUNICULAR_KEY,
    TROLLEY_BUS_KEY,
    MONORAIL_KEY,
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

    def test_process_routes_count_with_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

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
        mock_metadata.routes_count_by_type.assert_not_called()

    def test_process_routes_count_with_missing_fields(self):
        mock_routes = PropertyMock(return_value=pd.DataFrame({}))
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
        mock_metadata.routes_count_by_type.assert_not_called()

    def test_process_routes_count_by_type_with_some_routes(
        self,
    ):
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
        self.assertEqual(
            mock_metadata.routes_count_by_type,
            {
                TRAM_KEY: 5,
                SUBWAY_KEY: 1,
                RAIL_KEY: 1,
                CABLE_TRAM_KEY: 1,
                MONORAIL_KEY: 1,
            },
        )

    def test_process_routes_count_by_type_with_every_route(
        self,
    ):
        mock_routes = PropertyMock(
            return_value=pd.DataFrame(
                {ROUTE_TYPE: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
            )
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
        self.assertEqual(
            mock_metadata.routes_count_by_type,
            {
                TRAM_KEY: 1,
                SUBWAY_KEY: 1,
                RAIL_KEY: 1,
                BUS_KEY: 1,
                FERRY_KEY: 1,
                CABLE_TRAM_KEY: 1,
                AERIAL_LIFT_KEY: 1,
                FUNICULAR_KEY: 1,
                TROLLEY_BUS_KEY: 1,
                MONORAIL_KEY: 1,
            },
        )

    def test_process_routes_count_by_type_with_no_routes(
        self,
    ):
        mock_routes = PropertyMock(return_value=pd.DataFrame({ROUTE_TYPE: []}))
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
        mock_metadata.routes_count_by_type.assert_not_called()
