from unittest import TestCase, mock
from unittest.mock import MagicMock
from repository.data_repository import DataRepository
from representation.gtfs_representation import GtfsRepresentation


class DataRepositoryTest(TestCase):
    def test_data_repository_initializing_repository_should_return_instance(self):
        under_test = DataRepository()
        self.assertIsInstance(under_test, DataRepository)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_adding_none_dataset_key_should_raise_exception(
        self, mock_representation
    ):
        self.assertRaises(TypeError, DataRepository, None, mock_representation)

    def test_data_repository_adding_none_dataset_representation_should_raise_exception(
        self,
    ):
        mock_dataset_key = MagicMock()
        self.assertRaises(TypeError, DataRepository, mock_dataset_key, None)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_adding_representation_with_valid_parameters_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        under_test = DataRepository().add_dataset_representation(
            mock_dataset_key, mock_representation
        )
        self.assertIsNone(under_test)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_print_dataset_representations_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        under_test = DataRepository().print_all_dataset_representations()
        self.assertIsNone(under_test)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_print_dataset_representation_with_non_existent_key_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        mock_dataset_key.__str__.return_value = "test_key"

        test_dataset_key = "non_existent_test_key"

        data_repository = DataRepository()
        data_repository.add_dataset_representation(
            str(mock_dataset_key), mock_representation
        )
        under_test = data_repository.print_dataset_representation(test_dataset_key)
        self.assertIsNone(under_test)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_print_dataset_representation_with_existent_key_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        mock_dataset_key.__str__.return_value = "test_key"

        test_dataset_key = "test_key"

        data_repository = DataRepository()
        data_repository.add_dataset_representation(
            str(mock_dataset_key), mock_representation
        )
        under_test = data_repository.print_dataset_representation(test_dataset_key)
        self.assertIsNone(under_test)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_get_dataset_representations_should_return_representations(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        mock_dataset_key.__str__.return_value = "test_key"

        test_dataset_representations = {"test_key": mock_representation}

        data_repository = DataRepository()
        data_repository.add_dataset_representation(
            str(mock_dataset_key), mock_representation
        )
        under_test = data_repository.get_dataset_representations()
        self.assertEqual(under_test, test_dataset_representations)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_get_dataset_representation_with_non_existent_key_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        mock_dataset_key.__str__.return_value = "test_key"

        test_dataset_key = "non_existent_test_key"

        data_repository = DataRepository()
        data_repository.add_dataset_representation(
            str(mock_dataset_key), mock_representation
        )
        under_test = data_repository.get_dataset_representation(test_dataset_key)
        self.assertIsNone(under_test)

    @mock.patch("representation.gtfs_representation.GtfsRepresentation")
    def test_data_repository_get_dataset_representation_with_existent_key_should_return_none(
        self, mock_representation
    ):
        mock_representation.__class__ = GtfsRepresentation
        mock_dataset_key = MagicMock()
        mock_dataset_key.__class__ = str
        mock_dataset_key.__str__.return_value = "test_key"

        test_dataset_key = "test_key"
        test_dataset_representation = mock_representation

        data_repository = DataRepository()
        data_repository.add_dataset_representation(
            str(mock_dataset_key), mock_representation
        )
        under_test = data_repository.get_dataset_representation(test_dataset_key)
        self.assertEqual(under_test, test_dataset_representation)
