from unittest import TestCase
from unittest.mock import MagicMock
import os
import warnings
from usecase.download_dataset_as_zip import download_dataset_as_zip


def ignore_resource_warnings(test_func):
    """Removes the resource warnings raised by testing download execution (normal class behaviour).
    """
    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return test


class DownloadDatasetAsZipTest(TestCase):

    def test_download_dataset_with_none_path_to_data_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, download_dataset_as_zip, None, mock_urls)

    def test_download_dataset_with_invalid_path_to_data_should_raise_exception(self):
        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        self.assertRaises(TypeError, download_dataset_as_zip, mock_urls, mock_urls)

    def test_download_dataset_with_none_urls_should_raise_exception(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = './'
        self.assertRaises(TypeError, download_dataset_as_zip, str(mock_path_to_data), None)

    def test_download_dataset_with_invalid_urls_should_raise_exception(self):
        mock_path_to_data= MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = './'
        self.assertRaises(TypeError, download_dataset_as_zip, mock_path_to_data, mock_path_to_data)

    def test_download_dataset_with_valid_parameters_should_not_raise_exception(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict

        under_test = download_dataset_as_zip(str(mock_path_to_data), mock_urls)
        self.assertIsInstance(under_test, dict)

    def test_download_dataset_with_empty_urls_should_return_empty_zip_paths(self):
        test_zip_paths = {}
        test_urls = {}

        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__

        under_test = download_dataset_as_zip(str(mock_path_to_data), mock_urls)

        self.assertEqual(under_test, test_zip_paths)

    @ignore_resource_warnings
    def test_download_dataset_with_urls_should_return_zip_paths(self):
        test_zip_paths = {'url_key': './url_key_url_value.zip'}
        test_urls = {'url_key': 'http://test.com/url_value.zip'}

        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = './'

        mock_urls = MagicMock()
        mock_urls.__class__ = dict
        mock_urls.__getitem__.side_effect = test_urls.__getitem__
        mock_urls.items.return_value = test_urls.items()

        under_test = download_dataset_as_zip(str(mock_path_to_data), mock_urls)
        self.assertEqual(under_test, test_zip_paths)
        self.assertTrue(os.path.exists('./url_key_url_value.zip'))
        os.remove('./url_key_url_value.zip')
