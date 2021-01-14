import gtfs_kit
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation


class DatasetRepresentationFactory:
    def build_representation(self, dataset_type, entity_code, path_to_dataset, md5_hash, source_name, download_date):
        """Dataset representation builder method.
        The factory builds and return dataset representation accordingly to the dataset type.
        :param dataset_type: The type of the dataset, either GTFS or GBFS.
        :param entity_code: The entity code associated to the dataset in the database.
        :param path_to_dataset: The path to the dataset zip file to use for the representation.
        :param md5_hash: The MD5 hash of the dataset version.
        """
        representation = None
        try:
            if dataset_type == 'GTFS':
                dataset = gtfs_kit.read_feed(path_to_dataset, dist_units='km')
                metadata = GtfsMetadata(md5_hash, source_name, download_date)
                representation = GtfsRepresentation(entity_code, dataset, metadata)
            elif dataset_type == 'GBFS':
                # TODO
                pass
        except Exception as e:
            raise Exception("Exception \"%s\" occurred while building the dataset representation.\n" % e)
        return representation
