import pandas as pd
from unittest import TestCase, mock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from unittest.mock import PropertyMock, MagicMock
from usecase.process_country_codes_for_gtfs_metadata import (
    process_country_codes_for_gtfs_metadata,
    STOP_LAT,
    STOP_LON,
    RG_COUNTRY_CODE_KEY,
)


class TestProcessCountryCodesForGtfsMetadata(TestCase):
    def test_process_country_codes_with_none_gtfs_representation(
        self,
    ):
        self.assertRaises(TypeError, process_country_codes_for_gtfs_metadata, None)

    def test_process_country_codes_with_invalid_gtfs_representation(
        self,
    ):
        self.assertRaises(
            TypeError,
            process_country_codes_for_gtfs_metadata,
            "invalid_gtfs_representation",
        )

    @mock.patch("usecase.process_country_codes_for_gtfs_metadata.rg.search")
    def test_process_country_codes_with_empty_lat_lon(self, mock_rg):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame({STOP_LAT: [], STOP_LON: []})
        )

        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_country_codes_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_rg.assert_not_called()
        mock_metadata.country_codes.assert_not_called()

    @mock.patch("usecase.process_country_codes_for_gtfs_metadata.rg.search")
    def test_process_country_codes_with_invalid_lat_lon(self, mock_rg):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame({STOP_LAT: [850], STOP_LON: [-4000]})
        )

        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_country_codes_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_metadata.country_codes.assert_not_called()

    @mock.patch("usecase.process_country_codes_for_gtfs_metadata.rg.search")
    def test_process_country_codes_with_lat_lon(self, mock_rg):
        mock_stops = PropertyMock(
            return_value=pd.DataFrame({STOP_LAT: [45.446466], STOP_LON: [-73.603118]})
        )

        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_rg.return_value = [{RG_COUNTRY_CODE_KEY: "CA"}]

        under_test = process_country_codes_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.country_codes, ["CA"])

        mock_stops = PropertyMock(
            return_value=pd.DataFrame(
                {STOP_LAT: [45.446466, 40.730610], STOP_LON: [-73.603118, -73.935242]}
            )
        )

        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).stops = mock_stops

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        mock_rg.return_value = [
            {RG_COUNTRY_CODE_KEY: "CA"},
            {RG_COUNTRY_CODE_KEY: "US"},
        ]

        under_test = process_country_codes_for_gtfs_metadata(mock_gtfs_representation)
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(mock_metadata.country_codes, ["CA", "US"])
