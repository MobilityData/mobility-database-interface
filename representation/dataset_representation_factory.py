import gtfs_kit
from representation.gtfs_metadata import GtfsMetadata
from representation.gtfs_representation import GtfsRepresentation


class DatasetRepresentationFactory:
    def build_representation(self, dataset_type, entity_code, dataset_path, md5_hash):
        if dataset_type == 'GTFS':
            dataset = gtfs_kit.read_feed(dataset_path, dist_units='km')
            metadata = GtfsMetadata(md5_hash)
            representation = GtfsRepresentation(entity_code, dataset, metadata)
        elif dataset_type == 'GBFS':
            # TODO
            pass
        return representation
