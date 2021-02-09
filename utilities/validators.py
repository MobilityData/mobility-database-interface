from representation.gtfs_representation import GtfsRepresentation


def validate_gtfs_representation(gtfs_representation):
    if not isinstance(gtfs_representation, GtfsRepresentation):
        raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
    return True
