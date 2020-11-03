from repository.data_repository import DataRepository
from representation.representation_factory import RepresentationFactory


class LoadDataset:
    def __init__(self, data_repository, representation_factory, datasets, dataset_type):
        """Constructor for ``LoadDataset``.
        :param data_repository: Data repository containing the dataset representations.
        :param representation_factory: The factory to build the dataset representations.
        :param datasets: The dictionary of datasets to load. The key must be the entity code
        associated to the dataset in the database. The values must be composed of a path
        to the dataset zip file and a its MD5 hash.
        :param dataset_type: URLs of the datasets to download.
        """
        try:
            if data_repository is None or not isinstance(data_repository, DataRepository):
                raise TypeError("Data repository must be a valid DataRepository.")
            self.data_repository = data_repository
            if representation_factory is None or not isinstance(representation_factory, RepresentationFactory):
                raise TypeError("Representation factory must be a valid RepresentationFactory.")
            self.data_repository = data_repository
            if datasets is None or not isinstance(datasets, dict):
                raise TypeError("Datasets must be a valid dictionary.")
            self.datasets = datasets
            self.dataset_type = dataset_type
        except Exception as e:
            raise e
