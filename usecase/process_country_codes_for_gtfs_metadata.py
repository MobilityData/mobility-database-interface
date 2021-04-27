import reverse_geocoder as rg
from utilities.constants import STOP_LAT, STOP_LON
from utilities.validators import validate_gtfs_representation

RG_COUNTRY_CODE_KEY = "cc"


def process_country_codes_for_gtfs_metadata(gtfs_representation):
    """Process the country codes of a GTFS dataset using the latitude and longitude pairs
    from `stops` file from the GTFS dataset of the representation.
    Add the country codes to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Initialize the country codes set
    country_codes = set()

    # Make sure latitude and longitude columns are present in stops.txt before execution
    if {STOP_LAT, STOP_LON}.issubset(dataset.stops.columns):
        # Zip the latitude and longitude pairs in stops.txt
        coordinates = [
            (lat, lon)
            for lat, lon in zip(
                dataset.stops[STOP_LAT].tolist(), dataset.stops[STOP_LON].tolist()
            )
        ]

        # Compute the country codes from every latitude and longitude pairs in stops.txt
        if len(coordinates) != 0:
            infos = rg.search(coordinates)
            for info in infos:
                country_code = info.get(RG_COUNTRY_CODE_KEY, None)
                if country_code:
                    country_codes.add(country_code)

    # Set the country codes in the GTFS representation
    metadata.country_codes = country_codes

    return gtfs_representation
