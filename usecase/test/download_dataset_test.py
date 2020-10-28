from unittest import TestCase, mock
from unittest.mock import MagicMock
from repository.gtfs_data_repository import GtfsDataRepository
from usecase.download_dataset import DownloadDataset


class ExtractSourcesUrlTest(TestCase):

    def test_download_dataset_with_none_data_repository_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, DownloadDataset, None, mock_urls)

    def test_download_dataset_with_invalid_data_repository_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, DownloadDataset, mock_urls, mock_urls)

    @mock.patch('repository.gtfs_data_repository.GtfsDataRepository')
    def test_download_dataset_with_none_urls_should_raise_exception(self, mock_data_repository):
        mock_data_repository.__class__ = GtfsDataRepository
        self.assertRaises(TypeError, DownloadDataset, mock_data_repository, None)

    @mock.patch('repository.gtfs_data_repository.GtfsDataRepository')
    def test_download_dataset_with_invalid_urls_should_raise_exception(self, mock_data_repository):
        mock_data_repository.__class__ = GtfsDataRepository
        self.assertRaises(TypeError, DownloadDataset, mock_data_repository, mock_data_repository)

    @mock.patch('repository.gtfs_data_repository.GtfsDataRepository')
    def test_download_dataset_with_valid_parameters_should_not_raise_exception(self, mock_data_repository):
        mock_data_repository.__class__ = GtfsDataRepository
        mock_urls = MagicMock()
        mock_urls.__class__ = dict

        under_test = DownloadDataset(mock_data_repository, mock_urls)
        self.assertIsInstance(under_test, DownloadDataset)
        mock_data_repository.assert_not_called()

    @mock.patch('repository.gtfs_data_repository.GtfsDataRepository')
    def test_download_dataset_with_empty_urls_should_add_nothing_to_data_repo(self, mock_data_repository):
        test_datasets = {}
        test_urls = {}

        mock_data_repository.__class__ = GtfsDataRepository
        mock_data_repository.get_datasets.return_value = test_datasets
        mock_data_repository.add_dataset.side_effect = test_datasets.update({})

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__

        under_test = DownloadDataset(mock_data_repository, mock_urls).execute()

        self.assertEqual(under_test.get_datasets(), {})
        mock_data_repository.assert_not_called()

    @mock.patch('repository.gtfs_data_repository.GtfsDataRepository')
    def test_download_dataset_with_urls_should_add_datasets_to_data_repo(self, mock_data_repository):
        test_datasets = {}
        test_urls = {'url_key': 'url_value'}

        mock_data_repository.__class__ = GtfsDataRepository
        mock_data_repository.get_datasets.return_value = test_datasets
        mock_data_repository.add_dataset.side_effect = test_datasets.update({'dataset_key': 'dataset_value'})

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__
        mock_urls.items.return_value = test_urls.items()

        under_test = DownloadDataset(mock_data_repository, mock_urls).execute()
        self.assertEqual(under_test.get_datasets(), {'dataset_key': 'dataset_value'})
        mock_data_repository.add_dataset.assert_called_once()
