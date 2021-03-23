from utilities.constants import (
    STOP_KEY,
    STATION_KEY,
    ENTRANCE_KEY,
    STOP,
    STATION,
    ENTRANCE,
    LOCATION_TYPE,
)
from utilities.validators import validate_gtfs_representation


def process_stops_count_by_type_for_gtfs_metadata(gtfs_representation):
    """Process and count by type all the stops in the `stops` file from the GTFS dataset of the representation.
    Add the dictionary of the stops count to the representation metadata once processed.
    :return: The representation of the GTFS dataset post-execution.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Transform the blank location types to 0
    # According to the GTFS specification, blank location type is a Stop
    dataset.stops[LOCATION_TYPE] = dataset.stops[LOCATION_TYPE].fillna(0)
    dataset.stops = dataset.stops

    # Count stops by location type
    # Generic Node (3) and Boarding Area (4) are not considered
    # because they relate to an existing Stop or Station.
    stops_count = (
        dataset.stops[LOCATION_TYPE].loc[dataset.stops[LOCATION_TYPE] == STOP].size
    )
    stations_count = (
        dataset.stops[LOCATION_TYPE].loc[dataset.stops[LOCATION_TYPE] == STATION].size
    )
    entrances_count = (
        dataset.stops[LOCATION_TYPE].loc[dataset.stops[LOCATION_TYPE] == ENTRANCE].size
    )

    # Create the dictionary of stops count by type
    stops_count_by_type = {
        STOP_KEY: stops_count,
        STATION_KEY: stations_count,
        ENTRANCE_KEY: entrances_count,
    }

    metadata.stops_count_by_type = stops_count_by_type
    return gtfs_representation
