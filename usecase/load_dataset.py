from repository.data_repository import DataRepository
from representation.dataset_representation_factory import build_representation
from utilities.validators import validate_datasets_infos

GTFS_TYPE = "GTFS"
GBFS_TYPE = "GBFS"


def load_dataset(data_repository, datasets_infos, dataset_type):
    """Load the datasets in memory in the data repository.
    :param data_repository: Data repository containing the dataset representations.
    :param datasets_infos: A list of dataset infos, for the datasets to load.
    :param dataset_type: URLs of the datasets to download.
    :return: The data repository containing the loaded dataset representations.
    """
    if not isinstance(data_repository, DataRepository):
        raise TypeError("Data repository must be a valid DataRepository.")
    if dataset_type not in [GTFS_TYPE, GBFS_TYPE]:
        raise TypeError(
            f"Dataset type must be a valid dataset type - {GTFS_TYPE} or {GBFS_TYPE}."
        )
    validate_datasets_infos(datasets_infos)

    # Load the datasets indicated in datasets_infos
    for dataset_infos in datasets_infos:
        print(
            f"--------------- Loading dataset : {dataset_infos.zip_path} ---------------\n"
        )
        dataset_representation = build_representation(dataset_type, dataset_infos)
        data_repository.add_dataset_representation(
            dataset_infos.entity_code, dataset_representation
        )

    return data_repository
