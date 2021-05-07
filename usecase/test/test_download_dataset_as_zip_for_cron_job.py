import datetime
import os
from unittest import TestCase, mock
from unittest.mock import MagicMock

from representation.dataset_infos import DatasetInfos
from usecase.download_dataset_as_zip import (
    add_download_date_for_cron_job,
)
from usecase.download_dataset_as_zip import download_datasets_as_zip
from utilities.decorators import ignore_resource_warnings


class TestAddDownloadDateForCronJob(TestCase):
    @mock.patch("usecase.download_dataset_as_zip.date")
    def test_add_download_date_for_cron_job(self, mock_date):
        mock_date.today.return_value = datetime.date(2021, 1, 1)

        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos

        under_test = add_download_date_for_cron_job(mock_dataset_infos)
        self.assertEqual(under_test.download_date, "2021-01-01")


class TestDownloadDatasetAsZip(TestCase):
    def test_download_dataset_with_none_path_to_data_should_raise_exception(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError, download_datasets_as_zip, None, mock_datasets_infos
        )

    def test_download_dataset_with_invalid_path_to_data(self):
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = DatasetInfos
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError,
            download_datasets_as_zip,
            mock_datasets_infos,
            mock_datasets_infos,
        )

    def test_download_dataset_with_none_datasets_infos(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"
        self.assertRaises(
            TypeError, download_datasets_as_zip, str(mock_path_to_data), None
        )

    def test_download_dataset_with_invalid_urls(self):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"
        mock_dataset_infos = MagicMock()
        mock_dataset_infos.__class__ = str
        mock_datasets_infos = [mock_dataset_infos]
        self.assertRaises(
            TypeError, download_datasets_as_zip, mock_path_to_data, mock_datasets_infos
        )

        mock_datasets_infos = MagicMock()
        self.assertRaises(
            TypeError,
            download_datasets_as_zip,
            mock_path_to_data,
            str(mock_datasets_infos),
        )

    def test_download_dataset_with_empty_datasets_infos(
        self,
    ):
        mock_path_to_data = MagicMock()
        mock_path_to_data.__class__ = str
        mock_path_to_data.__str__.return_value = "./"

        mock_datasets_infos = []

        under_test = download_datasets_as_zip(
            str(mock_path_to_data), mock_datasets_infos
        )

        self.assertEqual(len(under_test), 0)

    @ignore_resource_warnings
    @mock.patch("usecase.download_dataset_as_zip.add_download_date_for_cron_job")
    def test_download_dataset_with_dataset_url(self, mock_date_func):
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

        mock_date_func.return_value = mock_dataset_infos

        under_test = download_datasets_as_zip(
            str(mock_path_to_data),
            mock_datasets_infos,
        )
        self.assertEqual(len(under_test), 1)

        under_test_dataset_info = under_test[0]
        self.assertEqual(under_test_dataset_info.zip_path, test_zip_path)
        self.assertTrue(os.path.exists("./test_entity_code_url_value.zip"))
        os.remove("./test_entity_code_url_value.zip")
