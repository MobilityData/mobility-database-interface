from unittest import TestCase, mock
from unittest.mock import MagicMock
from representation.gtfs_representation import GtfsRepresentation
from repository.data_repository import DataRepository
from usecase.load_dataset import load_dataset, GTFS_TYPE
from representation.dataset_infos import DatasetInfos


class TestLoadDataset(TestCase):
    def test_load_dataset_with_none_data_repository_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE
        self.assertRaises(
            TypeError, load_dataset, None, mock_datasets_infos, str(mock_datatype)
        )

    def test_load_dataset_with_invalid_data_repository_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE
        self.assertRaises(
            TypeError,
            load_dataset,
            mock_datasets_infos,
            mock_datasets_infos,
            str(mock_datatype),
        )

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_none_datasets_should_raise_exception(
        self, mock_data_repository
    ):
        mock_data_repository.__class__ = DataRepository
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE
        self.assertRaises(
            TypeError, load_dataset, mock_data_repository, None, str(mock_datatype)
        )

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_invalid_datasets_should_raise_exception(
        self, mock_data_repository
    ):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        mock_data_repository.__class__ = DataRepository
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE
        self.assertRaises(
            TypeError,
            load_dataset,
            mock_data_repository,
            mock_datasets_infos,
            str(mock_datatype),
        )

        mock_datasets_infos = MagicMock()
        self.assertRaises(
            TypeError,
            load_dataset,
            mock_data_repository,
            str(mock_datasets_infos),
            str(mock_datatype),
        )

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_none_dataset_type_should_raise_exception(
        self, mock_data_repository
    ):
        mock_data_repository.__class__ = DataRepository
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError, load_dataset, mock_data_repository, mock_datasets_infos, None
        )

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_invalid_dataset_type_should_raise_exception(
        self, mock_data_repository
    ):
        mock_data_repository.__class__ = DataRepository
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError,
            load_dataset,
            mock_data_repository,
            mock_datasets_infos,
            mock_datasets_infos,
        )

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_empty_datasets_should_add_nothing_to_data_repo(
        self, mock_data_repository
    ):
        test_dataset_representations = {}
        test_datasets = {}

        def add_dataset_representation_side_effect(key, value):
            test_dataset_representations.__setitem__(key, value)

        mock_data_repository.__class__ = DataRepository
        mock_data_repository.get_dataset_representations.return_value = (
            test_dataset_representations
        )
        mock_data_repository.add_dataset_representation.side_effect = (
            add_dataset_representation_side_effect
        )

        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE

        under_test = load_dataset(mock_data_repository, [], str(mock_datatype))

        self.assertEqual(under_test.get_dataset_representations(), {})
        mock_data_repository.assert_not_called()

    @mock.patch("repository.data_repository.DataRepository")
    def test_load_dataset_with_datasets_should_add_representation_to_data_repo(
        self, mock_data_repository
    ):
        test_dataset_representations = {}
        test_zip_path = "./"
        test_entity_code = "Q80"
        test_md5_hash = "test_md5"
        test_source_name = "test_name"
        test_download_date = "test_date"

        def add_dataset_representation_side_effect(key, value):
            test_dataset_representations.__setitem__(key, value)

        mock_data_repository.__class__ = DataRepository
        mock_data_repository.get_dataset_representations.return_value = (
            test_dataset_representations
        )
        mock_data_repository.add_dataset_representation.side_effect = (
            add_dataset_representation_side_effect
        )

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).entity_code = test_entity_code
        type(mock_dataset_infos).md5_hash = test_md5_hash
        type(mock_dataset_infos).source_name = test_source_name
        type(mock_dataset_infos).download_date = test_download_date
        mock_datasets_infos = [mock_dataset_infos]

        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = GTFS_TYPE

        under_test = load_dataset(
            mock_data_repository, mock_datasets_infos, str(mock_datatype)
        )

        self.assertTrue("Q80" in under_test.get_dataset_representations().keys())
        self.assertIsInstance(
            under_test.get_dataset_representations()["Q80"], GtfsRepresentation
        )
        mock_data_repository.add_dataset_representation.assert_called_once()
        mock_data_repository.assert_not_called()
