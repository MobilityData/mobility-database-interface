from unittest import TestCase
from unittest.mock import MagicMock
from usecase.process_md5 import ProcessMd5


class ProcessMd5Test(TestCase):

    def test_process_md5_with_none_parameters_should_raise_exception(self):
        self.assertRaises(TypeError, ProcessMd5, None, None)

    def test_process_md5_with_invalid_parameters_should_raise_exception(self):
        mock_datasets = MagicMock()
        mock_datasets.__class__ = list
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = list
        self.assertRaises(TypeError, ProcessMd5, mock_datasets, mock_md5_hashes)

    def test_process_md5_with_none_datasets_should_raise_exception(self):
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        self.assertRaises(TypeError, ProcessMd5, None, mock_md5_hashes)

    def test_process_md5_with_invalid_datasets_should_raise_exception(self):
        mock_datasets = MagicMock()
        mock_datasets.__class__ = list
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        self.assertRaises(TypeError, ProcessMd5, mock_datasets, mock_md5_hashes)

    def test_process_md5_with_none_md5_hashes_should_raise_exception(self):
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        self.assertRaises(TypeError, ProcessMd5, mock_datasets, None)

    def test_process_md5_with_invalid_md5_hashes_should_raise_exception(self):
        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = list
        self.assertRaises(TypeError, ProcessMd5, mock_datasets, mock_md5_hashes)

    def test_process_md5_with_valid_parameters_should_not_raise_exception(self):
        test_datasets = {'Q80': ''}
        test_md5_hashes = {'Q80': {''}}

        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datasets.keys.return_value = test_datasets.keys()

        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        mock_md5_hashes.keys.return_value = test_md5_hashes.keys()

        under_test = ProcessMd5(mock_datasets, mock_md5_hashes)
        self.assertIsInstance(under_test, ProcessMd5)
        mock_datasets.items.assert_not_called()
        mock_datasets.keys.assert_called_once()
        mock_md5_hashes.keys.assert_called_once()

    def test_process_md5_with_dataset_md5_not_in_md5_hashes_should_return_dataset(self):
        test_datasets = {'Q80': './usecase/test/resources/test.zip'}
        test_md5_hashes = {'Q80': {"test_md5_hash"}}

        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datasets.__getitem__.side_effect = test_datasets.__getitem__
        mock_datasets.items.return_value = test_datasets.items()
        mock_datasets.keys.return_value = test_datasets.keys()

        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        mock_md5_hashes.__getitem__.side_effect = test_md5_hashes.__getitem__
        mock_md5_hashes.keys.return_value = test_md5_hashes.keys()

        under_test = ProcessMd5(mock_datasets, mock_md5_hashes).execute()
        self.assertEqual(under_test.items(), {'Q80': './usecase/test/resources/test.zip'}.items())
        mock_datasets.items.assert_called_once()
        mock_datasets.keys.assert_called()
        mock_md5_hashes.keys.assert_called_once()

    def test_process_md5_with_dataset_md5_in_md5_hashes_should_remove_dataset(self):
        test_datasets = {'Q80': './usecase/test/resources/test.zip'}
        test_md5_hashes = {'Q80': {"d41d8cd98f00b204e9800998ecf8427e"}}

        mock_datasets = MagicMock()
        mock_datasets.__class__ = dict
        mock_datasets.__getitem__.side_effect = test_datasets.__getitem__
        mock_datasets.items.return_value = test_datasets.items()
        mock_datasets.keys.return_value = test_datasets.keys()
        mock_datasets.__delitem__.side_effect = test_datasets.__delitem__

        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        mock_md5_hashes.__getitem__.side_effect = test_md5_hashes.__getitem__
        mock_md5_hashes.keys.return_value = test_md5_hashes.keys()

        under_test = ProcessMd5(mock_datasets, mock_md5_hashes).execute()
        self.assertEqual(under_test.items(), {}.items())
        mock_datasets.items.assert_called_once()
        mock_datasets.keys.assert_called()
        mock_md5_hashes.keys.assert_called_once()
