from repository.data_repository import DataRepository
from representation.dataset_representation_factory import DatasetRepresentationFactory


class LoadDataset:
    def __init__(self, data_repository, dataset_representation_factory, datasets_infos, dataset_type):
        """Constructor for ``LoadDataset``.
        :param data_repository: Data repository containing the dataset representations.
        :param dataset_representation_factory: The factory to build the dataset representations.
        :param datasets_infos: The dictionary of datasets infos for the datasets to load.
        The key must be the entity code associated to the dataset in the database.
        The values must be composed of a path to the dataset zip file, its MD5 hash and its source name.
        :param dataset_type: URLs of the datasets to download.
        """
        try:
            if data_repository is None or not isinstance(data_repository, DataRepository):
                raise TypeError("Data repository must be a valid DataRepository.")
            self.data_repository = data_repository
            if dataset_representation_factory is None or not isinstance(dataset_representation_factory,
                                                                        DatasetRepresentationFactory):
                raise TypeError("Representation factory must be a valid RepresentationFactory.")
            self.dataset_representation_factory = dataset_representation_factory
            if datasets_infos is None or not isinstance(datasets_infos, dict):
                raise TypeError("Datasets must be a valid dictionary.")
            self.datasets_infos = datasets_infos
            if dataset_type is None or dataset_type not in ['GTFS', 'GBFS']:
                raise TypeError("Dataset type must be a valid dataset type - GTFS or GBFS.")
            self.dataset_type = dataset_type
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``LoadDataset`` use case.
        :return: The data repository containing the loaded dataset representations.
        """
        for entity_code, dataset_infos in self.datasets_infos.items():
            try:
                print("--------------- Loading dataset : %s ---------------\n" % dataset_infos['path'])
                dataset_representation = \
                    self.dataset_representation_factory.build_representation(self.dataset_type,
                                                                             entity_code,
                                                                             dataset_infos['path'],
                                                                             dataset_infos['md5'],
                                                                             dataset_infos['source_name'],
                                                                             dataset_infos['download_date'])
                self.data_repository.add_dataset_representation(entity_code, dataset_representation)
            except Exception as e:
                print("Exception \"%s\" occurred while loading dataset.\n" % e)

        return self.data_repository
