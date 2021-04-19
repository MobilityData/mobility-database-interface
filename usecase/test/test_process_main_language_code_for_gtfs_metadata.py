import pandas as pd
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock
from gtfs_kit.feed import Feed
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from usecase.process_main_language_code_for_gtfs_metadata import (
    process_main_language_code_for_gtfs_metadata,
    AGENCY_LANG,
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

    def test_process_main_language_code_with_missing_files(self):
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.main_language_code,
            "",
        )

    def test_process_main_language_code_with_missing_fields(self):
        mock_agency = PropertyMock(return_value=pd.DataFrame({}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.main_language_code,
            "",
        )

    def test_process_main_language_code_with_empty_file(self):
        mock_agency = PropertyMock(return_value=pd.DataFrame({AGENCY_LANG: []}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        self.assertEqual(
            mock_metadata.main_language_code,
            "",
        )

    def test_process_main_language_code(self):
        mock_agency = PropertyMock(return_value=pd.DataFrame({AGENCY_LANG: ["fr"]}))
        mock_dataset = MagicMock()
        mock_dataset.__class__ = Feed
        type(mock_dataset).agency = mock_agency

        mock_metadata = MagicMock()
        mock_metadata.__class__ = GtfsMetadata

        mock_gtfs_representation = MagicMock()
        mock_gtfs_representation.__class__ = GtfsRepresentation
        type(mock_gtfs_representation).dataset = mock_dataset
        type(mock_gtfs_representation).metadata = mock_metadata

        under_test = process_main_language_code_for_gtfs_metadata(
            mock_gtfs_representation
        )
        self.assertIsInstance(under_test, GtfsRepresentation)
        mock_agency.assert_called()
        self.assertEqual(mock_metadata.main_language_code, "fr")
