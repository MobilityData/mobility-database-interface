from unittest import TestCase, mock
from unittest.mock import MagicMock
from representation.dataset_representation_factory import (
    build_representation,
    GTFS_TYPE,
    GBFS_TYPE,
)
from representation.gtfs_representation import GtfsRepresentation
from representation.dataset_infos import DatasetInfos
from requests.exceptions import MissingSchema


class DatasetRepresentationFactoryTest(TestCase):
    def test_build_representation_with_none_dataset_type_should_return_none(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        under_test = build_representation(None, mock_dataset_infos)
        self.assertIsNone(under_test)

    def test_build_representation_with_invalid_dataset_type_should_return_none(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        test_dataset_type = "invalid_dataset_type"

        under_test = build_representation(test_dataset_type, mock_dataset_infos)
        self.assertIsNone(under_test)

    def test_build_gtfs_representation_with_none_dataset_infos_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = GTFS_TYPE

        self.assertRaises(TypeError, build_representation, str(mock_dataset_type), None)

    def test_build_gtfs_representation_with_invalid_dataset_infos_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = GTFS_TYPE

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str

        self.assertRaises(
            TypeError, build_representation, str(mock_dataset_type), mock_dataset_infos
        )

    def test_build_gtfs_representation_with_invalid_path_to_dataset_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = GTFS_TYPE

        test_path_to_dataset = "invalid_path_to_dataset"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_path_to_dataset

        self.assertRaises(
            MissingSchema,
            build_representation,
            str(mock_dataset_type),
            mock_dataset_infos,
        )

    def test_build_gtfs_representation_with_valid_parameters_should_return_gtfs_representation(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = GTFS_TYPE

        test_entity_code = "test_entity_code"
        test_zip_path = "./representation/test/resources/citcrc.zip"
        test_md5_hash = "test_md5_hash"
        test_source_name = "test_source_name"
        test_download_date = "test_download_date"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).entity_code = test_entity_code
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).md5_hash = test_md5_hash
        type(mock_dataset_infos).source_name = test_source_name
        type(mock_dataset_infos).download_date = test_download_date

        under_test = build_representation(str(mock_dataset_type), mock_dataset_infos)
        self.assertIsInstance(under_test, GtfsRepresentation)

    def test_build_gbfs_representation_should_raise_exception(self):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = GBFS_TYPE

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        self.assertRaises(
            NotImplementedError,
            build_representation,
            str(mock_dataset_type),
            mock_dataset_infos,
        )
