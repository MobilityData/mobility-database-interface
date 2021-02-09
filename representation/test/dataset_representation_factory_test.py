from unittest import TestCase, mock
from unittest.mock import MagicMock
from representation.dataset_representation_factory import DatasetRepresentationFactory
from representation.gtfs_representation import GtfsRepresentation


class DatasetRepresentationFactoryTest(TestCase):
    def test_build_representation_with_none_dataset_type_should_return_none(self):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        dataset_representation_factory = DatasetRepresentationFactory()
        under_test = dataset_representation_factory.build_representation(
            None, mock_entity_code, mock_path_to_dataset, mock_md5_hash
        )
        self.assertIsNone(under_test)

    def test_build_representation_with_invalid_dataset_type_should_return_none(self):
        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        test_dataset_type = "invalid_dataset_type"

        dataset_representation_factory = DatasetRepresentationFactory()
        under_test = dataset_representation_factory.build_representation(
            test_dataset_type, mock_entity_code, mock_path_to_dataset, mock_md5_hash
        )
        self.assertIsNone(under_test)

    def test_build_gtfs_representation_with_none_path_to_dataset_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            mock_entity_code,
            None,
            mock_md5_hash,
        )

    def test_build_gtfs_representation_with_invalid_path_to_dataset_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        test_path_to_dataset = "invalid_path_to_dataset"

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            mock_entity_code,
            test_path_to_dataset,
            mock_md5_hash,
        )

    def test_build_gtfs_representation_with_none_md5_should_raise_exception(self):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_path_to_dataset.__str__.return_value = (
            "./representation/test/resources/citcrc.zip"
        )

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            mock_entity_code,
            str(mock_path_to_dataset),
            None,
        )

    def test_build_gtfs_representation_with_invalid_md5_should_raise_exception(self):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_path_to_dataset.__str__.return_value = (
            "./representation/test/resources/citcrc.zip"
        )

        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = int

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            mock_entity_code,
            str(mock_path_to_dataset),
            mock_md5_hash,
        )

    def test_build_gtfs_representation_with_none_entity_code_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_path_to_dataset.__str__.return_value = (
            "./representation/test/resources/citcrc.zip"
        )

        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            None,
            str(mock_path_to_dataset),
            mock_md5_hash,
        )

    def test_build_gtfs_representation_with_invalid_entity_code_should_raise_exception(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = int

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_path_to_dataset.__str__.return_value = (
            "./representation/test/resources/citcrc.zip"
        )

        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        dataset_representation_factory = DatasetRepresentationFactory()
        self.assertRaises(
            Exception,
            dataset_representation_factory.build_representation,
            str(mock_dataset_type),
            mock_entity_code,
            str(mock_path_to_dataset),
            mock_md5_hash,
        )

    def test_build_gtfs_representation_with_valid_parameters_should_return_gtfs_representation(
        self,
    ):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GTFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str
        mock_entity_code.__str__.return_value = "test_entity_code"

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str
        mock_path_to_dataset.__str__.return_value = (
            "./representation/test/resources/citcrc.zip"
        )

        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str
        mock_md5_hash.__str__.return_value = "test_md5_hash"

        dataset_representation_factory = DatasetRepresentationFactory()
        under_test = dataset_representation_factory.build_representation(
            str(mock_dataset_type),
            str(mock_entity_code),
            str(mock_path_to_dataset),
            str(mock_md5_hash),
        )
        self.assertIsInstance(under_test, GtfsRepresentation)

    def test_build_gbfs_representation_should_return_none(self):
        mock_dataset_type = MagicMock()
        mock_dataset_type.__class__ = str
        mock_dataset_type.__str__.return_value = "GBFS"

        mock_entity_code = MagicMock()
        mock_entity_code.__class__ = str

        mock_path_to_dataset = MagicMock()
        mock_path_to_dataset.__class__ = str

        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        dataset_representation_factory = DatasetRepresentationFactory()
        under_test = dataset_representation_factory.build_representation(
            str(mock_dataset_type),
            mock_entity_code,
            mock_path_to_dataset,
            mock_md5_hash,
        )
        self.assertIsNone(under_test)
