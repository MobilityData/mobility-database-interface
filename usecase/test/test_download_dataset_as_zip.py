from unittest import TestCase
from unittest.mock import MagicMock
import os
import warnings
from representation.dataset_infos import DatasetInfos
from usecase.download_dataset_as_zip import download_dataset_as_zip


def ignore_resource_warnings(test_func):
    """Removes the resource warnings raised by testing download execution (normal class behaviour)."""

    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return test


class TestDownloadDatasetAsZip(TestCase):
    def test_download_dataset_with_none_path_to_data_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(TypeError, download_dataset_as_zip, None, mock_datasets_infos)

    def test_download_dataset_with_invalid_path_to_data_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError, download_dataset_as_zip, mock_datasets_infos, mock_datasets_infos
        )

    def test_download_dataset_with_none_datasets_infos_should_raise_exception(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"
        self.assertRaises(
            TypeError, download_dataset_as_zip, str(mock_path_to_data), None
        )

    def test_download_dataset_with_invalid_urls_should_raise_exception(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError, download_dataset_as_zip, mock_path_to_data, mock_datasets_infos
        )

        mock_datasets_infos = MagicMock()
        self.assertRaises(
            TypeError,
            download_dataset_as_zip,
            mock_path_to_data,
            str(mock_datasets_infos),
        )

    def test_download_dataset_with_empty_datasets_infos_should_return_empty_datasets_infos(
        self,
    ):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"

        mock_datasets_infos = []

        under_test = download_dataset_as_zip(
            str(mock_path_to_data), mock_datasets_infos
        )

        self.assertEqual(len(under_test), 0)

    @ignore_resource_warnings
    def test_download_dataset_with_dataset_url_should_return_updated_datasets_infos(
        self,
    ):
        test_entity_code = "test_entity_code"
        test_url = "http://test.com/url_value.zip"
        test_zip_path = "./test_entity_code_url_value.zip"

        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        type(mock_dataset_infos).entity_code = test_entity_code
        type(mock_dataset_infos).url = test_url
        mock_datasets_infos = [mock_dataset_infos]

        under_test = download_dataset_as_zip(
            str(mock_path_to_data), mock_datasets_infos
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.zip_path, test_zip_path)
        self.assertTrue(os.path.exists("./test_entity_code_url_value.zip"))
        os.remove("./test_entity_code_url_value.zip")
