import gtfs_kit
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from representation.dataset_infos import DatasetInfos
from requests.exceptions import MissingSchema

GTFS_TYPE = "GTFS"
GBFS_TYPE = "GBFS"


def build_representation(dataset_type, dataset_infos):
    """Dataset representation builder function.
    The factory builds and return a dataset representation according to the dataset type.
    :param dataset_type: The type of the dataset, either GTFS or GBFS.
    :param dataset_infos: The processing infos of the dataset.
    """
    if not isinstance(dataset_infos, DatasetInfos):
        raise TypeError("Dataset infos must be a valid DatasetInfos.")

    representation = None
    if dataset_type == GTFS_TYPE:
        representation = build_gtfs_representation(dataset_infos)
    elif dataset_type == GBFS_TYPE:
        representation = build_gbfs_representation(dataset_infos)
    return representation


def build_gtfs_representation(dataset_infos):
    try:
        dataset = gtfs_kit.read_feed(dataset_infos.zip_path, dist_units="km")
    except TypeError as te:
        raise TypeError(
            f"Exception '{te}' occurred while reading the GTFS dataset with the GTFS kit library."
            f"The dataset must be a valid GTFS zip file or URL.\n"
        )
    except MissingSchema as ms:
        raise MissingSchema(
            f"Exception '{ms}' occurred while opening the GTFS dataset with the GTFS kit library."
            f"The dataset must be a valid GTFS zip file or URL.\n"
        )
    metadata = GtfsMetadata(dataset_infos)
    representation = GtfsRepresentation(dataset_infos.entity_code, dataset, metadata)
    return representation


def build_gbfs_representation(dataset_infos):
    raise NotImplementedError
