from unittest import TestCase
from unittest.mock import MagicMock
from usecase.process_md5 import process_datasets_md5
from representation.dataset_infos import DatasetInfos


class TestProcessMd5(TestCase):
    def test_process_datasets_md5_with_none_parameters_should_raise_exception(self):
        self.assertRaises(TypeError, process_datasets_md5, None)

    def test_process_datasets_md5_with_invalid_parameters_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(TypeError, process_datasets_md5, mock_datasets_infos)

        mock_datasets_infos = MagicMock()
        self.assertRaises(TypeError, process_datasets_md5, str(mock_datasets_infos))

    def test_process_datasets_md5_with_dataset_md5_not_in_md5_hashes_should_return_dataset(
        self,
    ):
        test_zip_path = "./usecase/test/resources/test.zip"
        test_previous_md5_hashes = {"test_md5_hash"}
        test_md5_hash = "d41d8cd98f00b204e9800998ecf8427e"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).previous_md5_hashes = test_previous_md5_hashes
        mock_datasets_infos = [mock_dataset_infos]

        under_test = process_datasets_md5(mock_datasets_infos)
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.md5_hash, test_md5_hash)

    def test_process_datasets_md5_with_dataset_md5_existing_in_md5_hashes_should_discard_dataset(
        self,
    ):
        test_zip_path = "./usecase/test/resources/test.zip"
        test_previous_md5_hashes = {"d41d8cd98f00b204e9800998ecf8427e"}

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).previous_md5_hashes = test_previous_md5_hashes
        mock_datasets_infos = [mock_dataset_infos]

        under_test = process_datasets_md5(mock_datasets_infos)
        self.assertEqual(len(under_test), 0)
