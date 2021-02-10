import gtfs_kit
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation
from requests.exceptions import MissingSchema

GTFS_TYPE = "GTFS"
GBFS_TYPE = "GBFS"


def build_representation(dataset_type, entity_code, path_to_dataset, md5_hash):
    """Dataset representation builder function.
    The factory builds and return a dataset representation according to the dataset type.
    :param dataset_type: The type of the dataset, either GTFS or GBFS.
    :param entity_code: The entity code associated to the dataset in the database.
    :param path_to_dataset: The path to the dataset zip file to use for the representation.
    :param md5_hash: The MD5 hash of the dataset version.
    """
    representation = None
    if dataset_type == GTFS_TYPE:
        representation = build_gtfs_representation(
            entity_code, path_to_dataset, md5_hash
        )
    elif dataset_type == GBFS_TYPE:
        representation = build_gbfs_representation(
            entity_code, path_to_dataset, md5_hash
        )
    return representation


def build_gtfs_representation(entity_code, path_to_dataset, md5_hash):
    try:
        dataset = gtfs_kit.read_feed(path_to_dataset, dist_units="km")
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
    metadata = GtfsMetadata(md5_hash)
    representation = GtfsRepresentation(entity_code, dataset, metadata)
    return representation


def build_gbfs_representation(entity_code, path_to_dataset, md5_hash):
    raise NotImplementedError
