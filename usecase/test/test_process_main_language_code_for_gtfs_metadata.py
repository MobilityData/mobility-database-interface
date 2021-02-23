import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
)


class TestProcessMainLanguageCodeForGtfsMetadata(TestCase):
    def test_process_main_language_code_with_none(self):
        self.assertRaises(TypeError, process_main_language_code_for_gtfs_metadata, None)

    def test_process_main_language_code_with_invalid_gtfs_repr(self):
        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = str
        self.assertRaises(
            TypeError,
            process_main_language_code_for_gtfs_metadata,
            mock_gtfs_representation,
        )

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_process_main_language_code_with_valid_gtfs_representation_should_return_instance(
        self, mock_gtfs_representation
    ):
        mock_gtfs_representation.__class__ = GtfsRepresentation
        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    @mock.patch("gtfs_kit.feed.Feed")
    @mock.patch("representation.gtfs_metadata.GtfsMetadata")
    def test_process_main_language_code(
        self, mock_gtfs_representation, mock_dataset, mock_metadata
    ):
        mock_agency = PropertyMock(return_value=pd.DataFrame({"agency_lang": ["fr"]}))
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata.__class__ = GtfsMetadata
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_agency.assert_called()
        self.assertEqual(mock_agency.call_count, 1)
        self.assertEqual(mock_metadata.main_language_code, "fr")
