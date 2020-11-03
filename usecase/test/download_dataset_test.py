from unittest import TestCase
from unittest.mock import MagicMock
import os
import warnings
from usecase.download_dataset import DownloadDataset


def ignore_resource_warnings(test_func):
    """Removes the resource warnings raised by testing download execution (normal class behaviour).
    """
    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return test


class ExtractSourcesUrlTest(TestCase):

    def test_download_dataset_with_none_data_folder_path_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, DownloadDataset, None, mock_urls)

    def test_download_dataset_with_invalid_data_folder_path_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, DownloadDataset, mock_urls, mock_urls)

    def test_download_dataset_with_none_urls_should_raise_exception(self):
        mock_data_folder_path = MagicMock()
        mock_data_folder_path.__class__ = str
        mock_data_folder_path.__str__.return_value = './'
        self.assertRaises(TypeError, DownloadDataset, str(mock_data_folder_path), None)

    def test_download_dataset_with_invalid_urls_should_raise_exception(self):
        mock_data_folder_path = MagicMock()
        mock_data_folder_path.__class__ = str
        mock_data_folder_path.__str__.return_value = './'
        self.assertRaises(TypeError, DownloadDataset, mock_data_folder_path, mock_data_folder_path)

    def test_download_dataset_with_valid_parameters_should_not_raise_exception(self):
        mock_data_folder_path = MagicMock()
        mock_data_folder_path.__class__ = str
        mock_data_folder_path.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict

        under_test = DownloadDataset(str(mock_data_folder_path), mock_urls)
        self.assertIsInstance(under_test, DownloadDataset)

    def test_download_dataset_with_empty_urls_should_return_empty_zip_paths(self):
        test_datasets = {}
        test_urls = {}

        mock_data_folder_path = MagicMock()
        mock_data_folder_path.__class__ = str
        mock_data_folder_path.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__

        under_test = DownloadDataset(str(mock_data_folder_path), mock_urls).execute()

        self.assertEqual(under_test, test_datasets)

    @ignore_resource_warnings
    def test_download_dataset_with_urls_should_add_datasets_to_data_repo(self):
        test_datasets = {'url_key': './url_key_url_value.zip'}
        test_urls = {'url_key': 'http://test.com/url_value.zip'}

        mock_data_folder_path = MagicMock()
        mock_data_folder_path.__class__ = str
        mock_data_folder_path.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__
        mock_urls.items.return_value = test_urls.items()

        under_test = DownloadDataset(str(mock_data_folder_path), mock_urls).execute()
        self.assertEqual(under_test, test_datasets)
        self.assertTrue(os.path.exists('./url_key_url_value.zip'))
        os.remove('./url_key_url_value.zip')
