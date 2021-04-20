from unittest import TestCase
from unittest.mock import MagicMock
from usecase.process_sha1 import process_sha1
from representation.dataset_infos import DatasetInfos


class TestProcessSha1(TestCase):
    def test_process_sha1_with_none_parameters_should_raise_exception(self):
        self.assertRaises(TypeError, process_sha1, None)

    def test_process_sha1_with_invalid_parameters_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(TypeError, process_sha1, mock_datasets_infos)

        mock_datasets_infos = MagicMock()
        self.assertRaises(TypeError, process_sha1, str(mock_datasets_infos))

    def test_process_sha1_with_dataset_sha1_not_in_sha1_hashes_should_return_dataset(
        self,
    ):
        test_zip_path = "./usecase/test/resources/test.zip"
        test_previous_sha1_hashes = {"test_sha1_hash"}
        test_sha1_hash = "da39a3ee5e6b4b0d3255bfef95601890afd80709"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).previous_sha1_hashes = test_previous_sha1_hashes
        mock_datasets_infos = [mock_dataset_infos]

        under_test = process_sha1(mock_datasets_infos)
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.sha1_hash, test_sha1_hash)

    def test_process_md5_with_dataset_md5_existing_in_md5_hashes_should_discard_dataset(
        self,
    ):
        test_zip_path = "./usecase/test/resources/test.zip"
        test_previous_sha1_hashes = {"da39a3ee5e6b4b0d3255bfef95601890afd80709"}

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        type(mock_dataset_infos).zip_path = test_zip_path
        type(mock_dataset_infos).previous_sha1_hashes = test_previous_sha1_hashes
        mock_datasets_infos = [mock_dataset_infos]

        under_test = process_sha1(mock_datasets_infos)
        self.assertEqual(len(under_test), 0)
