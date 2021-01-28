from repository.data_repository import DataRepository
from representation.dataset_representation_factory import DatasetRepresentationFactory

PATH_TO_DATASET_KEY = "path"
MD5_HASH_KEY = "md5"
GTFS_TYPE = "GTFS"
GBFS_TYPE = "GBFS"


def load_dataset(data_repository, dataset_representation_factory, datasets_infos, dataset_type):
    """Load the datasets in memory in the data repository.
    :param data_repository: Data repository containing the dataset representations.
    :param dataset_representation_factory: The factory to build the dataset representations.
    :param datasets_infos: The dictionary of datasets infos to load. The key must be the entity code
    associated to the dataset in the database. The values must be composed of a path
    to the dataset zip file and a its MD5 hash.
    :param dataset_type: URLs of the datasets to download.
    :return: The data repository containing the loaded dataset representations.
    """
    if not isinstance(data_repository, DataRepository):
        raise TypeError("Data repository must be a valid DataRepository.")
    if not isinstance(dataset_representation_factory, DatasetRepresentationFactory):
        raise TypeError("Representation factory must be a valid RepresentationFactory.")
    if (
            not isinstance(datasets_infos, dict)
            and not all(key in datasets_infos for key in (PATH_TO_DATASET_KEY, MD5_HASH_KEY))
    ):
        raise TypeError(f"Datasets must be a valid dictionary, with keys {PATH_TO_DATASET_KEY} and {MD5_HASH_KEY}.")
    if dataset_type not in [GTFS_TYPE, GBFS_TYPE]:
        raise TypeError(f"Dataset type must be a valid dataset type - {GTFS_TYPE} or {GBFS_TYPE}.")

    # Load the datasets indicated in datasets_infos
    for entity_code, dataset_infos in datasets_infos.items():
        print(f"--------------- Loading dataset : {dataset_infos['path']} ---------------\n")
        dataset_representation = dataset_representation_factory.build_representation(dataset_type,
                                                                                     entity_code,
                                                                                     dataset_infos['path'],
                                                                                     dataset_infos['md5'])
        data_repository.add_dataset_representation(entity_code, dataset_representation)

    return data_repository
