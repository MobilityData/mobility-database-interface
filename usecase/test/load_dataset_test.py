from unittest import TestCase, mock
from unittest.mock import MagicMock
from repository.data_repository import DataRepository
from representation.dataset_representation_factory import DatasetRepresentationFactory
from usecase.load_dataset import LoadDataset


class LoadDatasetTest(TestCase):

    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_none_data_repository_should_raise_exception(self, mock_factory):
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, None, mock_factory, mock_datasets, str(mock_datatype))

    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_invalid_data_repository_should_raise_exception(self, mock_factory):
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, mock_factory, mock_factory, mock_datasets, str(mock_datatype))

    @mock.patch('repository.data_repository.DataRepository')
    def test_load_dataset_with_none_representation_factory_should_raise_exception(self, mock_data_repository):
        mock_data_repository.__class__ = DataRepository
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, None, mock_datasets, str(mock_datatype))

    @mock.patch('repository.data_repository.DataRepository')
    def test_load_dataset_with_invalid_representation_factory_should_raise_exception(self, mock_data_repository):
        mock_data_repository.__class__ = DataRepository
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, mock_data_repository,
                          mock_datasets, str(mock_datatype))

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_none_datasets_should_raise_exception(self, mock_data_repository, mock_factory):
        mock_data_repository.__class__ = DataRepository
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, mock_factory, None, str(mock_datatype))

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_invalid_datasets_should_raise_exception(self, mock_data_repository, mock_factory):
        mock_data_repository.__class__ = DataRepository
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, mock_factory,
                          mock_factory, str(mock_datatype))

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_none_dataset_type_should_raise_exception(self, mock_data_repository, mock_factory):
        mock_data_repository.__class__ = DataRepository
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, mock_factory, mock_datasets, None)

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_invalid_dataset_type_should_raise_exception(self, mock_data_repository, mock_factory):
        mock_data_repository.__class__ = DataRepository
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        self.assertRaises(TypeError, LoadDataset, mock_data_repository, mock_factory, mock_datasets, mock_datasets)

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_valid_parameters_should_not_raise_exception(self, mock_data_repository, mock_factory):
        mock_data_repository.__class__ = DataRepository
        mock_factory.__class__ = DatasetRepresentationFactory
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'

        under_test = LoadDataset(mock_data_repository, mock_factory, mock_datasets, str(mock_datatype))
        self.assertIsInstance(under_test, LoadDataset)

    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_empty_datasets_should_add_nothing_to_data_repo(self, mock_data_repository, mock_factory):
        test_dataset_representations = {}
        test_datasets = {}

        def add_dataset_representation_side_effect(key, value):
            test_dataset_representations.__setitem__(key, value)

        mock_data_repository.__class__ = DataRepository
        mock_data_repository.get_dataset_representations.return_value = test_dataset_representations
        mock_data_repository.add_dataset_representation.side_effect = add_dataset_representation_side_effect

        mock_factory.__class__ = DatasetRepresentationFactory
        mock_factory.build_representation.return_value = 'test_representation'

        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datasets.__getitem__.side_effect = test_datasets.__getitem__
        mock_datasets.items.return_value = test_datasets.items()

        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'

        under_test = LoadDataset(mock_data_repository, mock_factory, mock_datasets, str(mock_datatype)).execute()

        self.assertEqual(under_test.get_dataset_representations(), {})
        mock_data_repository.assert_not_called()


    @mock.patch('repository.data_repository.DataRepository')
    @mock.patch('representation.dataset_representation_factory.DatasetRepresentationFactory')
    def test_load_dataset_with_datasets_should_add_representation_to_data_repo(self, mock_data_repository,
                                                                               mock_factory):
        test_dataset_representations = {}
        test_datasets = {'Q80': {'path': './', 'md5': 'test_md5'}}

        def add_dataset_representation_side_effect(key, value):
            test_dataset_representations.__setitem__(key, value)

        mock_data_repository.__class__ = DataRepository
        mock_data_repository.get_dataset_representations.return_value = test_dataset_representations
        mock_data_repository.add_dataset_representation.side_effect = add_dataset_representation_side_effect

        mock_factory.__class__ = DatasetRepresentationFactory
        mock_factory.build_representation.return_value = 'test_representation'

        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datasets.__getitem__.side_effect = test_datasets.__getitem__
        mock_datasets.items.return_value = test_datasets.items()

        mock_datatype = MagicMock()
        mock_datatype.__class__ = str
        mock_datatype.__str__.return_value = 'GTFS'

        under_test = LoadDataset(mock_data_repository, mock_factory, mock_datasets, str(mock_datatype)).execute()

        self.assertEqual(under_test.get_dataset_representations(), {'Q80': 'test_representation'})
        mock_factory.build_representation.assert_called_once()
        mock_data_repository.add_dataset_representation.assert_called_once()
        mock_data_repository.assert_not_called()
