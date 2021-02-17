from unittest import TestCase
from unittest.mock import MagicMock
from usecase.process_md5 import process_md5


class TestProcessMd5(TestCase):
    def test_process_md5_with_none_parameters_should_raise_exception(self):
        self.assertRaises(TypeError, process_md5, None, None)

    def test_process_md5_with_invalid_parameters_should_raise_exception(self):
        mock_datasets = MagicMock()
        mock_datasets.__class__ = list
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = list
        self.assertRaises(TypeError, process_md5, mock_datasets, mock_md5_hashes)

    def test_process_md5_with_none_paths_to_datasets_should_raise_exception(self):
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        self.assertRaises(TypeError, process_md5, None, mock_md5_hashes)

    def test_process_md5_with_invalid_paths_to_datasets_should_raise_exception(self):
        mock_paths_to_datasets = MagicMock()
        mock_paths_to_datasets.__class__ = list
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        self.assertRaises(
            TypeError, process_md5, mock_paths_to_datasets, mock_md5_hashes
        )

    def test_process_md5_with_none_md5_hashes_should_raise_exception(self):
        mock_paths_to_datasets = MagicMock()
        mock_paths_to_datasets.__class__ = dict
        self.assertRaises(TypeError, process_md5, mock_paths_to_datasets, None)

    def test_process_md5_with_invalid_md5_hashes_should_raise_exception(self):
        mock_paths_to_datasets = MagicMock()
        mock_paths_to_datasets.__class__ = dict
        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = list
        self.assertRaises(
            TypeError, process_md5, mock_paths_to_datasets, mock_md5_hashes
        )

    def test_process_md5_with_dataset_md5_not_in_md5_hashes_should_return_dataset(self):
        test_paths_to_datasets = {"Q80": "./usecase/test/resources/test.zip"}
        test_md5_hashes = {"Q80": {"test_md5_hash"}}
        test_paths_to_datasets_and_md5 = {
            "Q80": {
                "path": "./usecase/test/resources/test.zip",
                "md5": "d41d8cd98f00b204e9800998ecf8427e",
            }
        }

        mock_paths_to_datasets = MagicMock()
        mock_paths_to_datasets.__class__ = dict
        mock_paths_to_datasets.__getitem__.side_effect = (
            test_paths_to_datasets.__getitem__
        )
        mock_paths_to_datasets.items.return_value = test_paths_to_datasets.items()
        mock_paths_to_datasets.keys.return_value = test_paths_to_datasets.keys()

        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        mock_md5_hashes.__getitem__.side_effect = test_md5_hashes.__getitem__
        mock_md5_hashes.keys.return_value = test_md5_hashes.keys()

        under_test = process_md5(mock_paths_to_datasets, mock_md5_hashes)
        self.assertEqual(under_test.items(), test_paths_to_datasets_and_md5.items())
        mock_paths_to_datasets.keys.assert_called()
        mock_md5_hashes.keys.assert_called_once()

    def test_process_md5_with_dataset_md5_existing_in_md5_hashes_should_discard_dataset(
        self,
    ):

        test_paths_to_datasets = {"Q80": "./usecase/test/resources/test.zip"}
        test_md5_hashes = {"Q80": {"d41d8cd98f00b204e9800998ecf8427e"}}
        test_paths_to_datasets_and_md5 = {}

        mock_paths_to_datasets = MagicMock()
        mock_paths_to_datasets.__class__ = dict
        mock_paths_to_datasets.__getitem__.side_effect = (
            test_paths_to_datasets.__getitem__
        )
        mock_paths_to_datasets.items.return_value = test_paths_to_datasets.items()
        mock_paths_to_datasets.keys.return_value = test_paths_to_datasets.keys()
        mock_paths_to_datasets.__delitem__.side_effect = (
            test_paths_to_datasets.__delitem__
        )

        mock_md5_hashes = MagicMock()
        mock_md5_hashes.__class__ = dict
        mock_md5_hashes.__getitem__.side_effect = test_md5_hashes.__getitem__
        mock_md5_hashes.keys.return_value = test_md5_hashes.keys()

        under_test = process_md5(mock_paths_to_datasets, mock_md5_hashes)
        self.assertEqual(under_test.items(), test_paths_to_datasets_and_md5.items())
        mock_paths_to_datasets.keys.assert_called()
        mock_md5_hashes.keys.assert_called_once()
