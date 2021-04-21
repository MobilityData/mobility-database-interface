from utilities.validators import validate_gtfs_representation
from utilities.constants import STOP_TIMEZONE, AGENCY_TIMEZONE

AGENCY_TIMEZONE_IDX = 0


def process_timezones_for_gtfs_metadata(gtfs_representation):
    """Process all the timezones using the `stops` and the `agency` files from the GTFS dataset of the representation.
    Add the list of all the timezones to the representation metadata once processed.
    :param gtfs_representation: The representation of the GTFS dataset to process.
    :return: The representation of the GTFS dataset post-execution.
    """
    validate_gtfs_representation(gtfs_representation)
    dataset = gtfs_representation.dataset
    metadata = gtfs_representation.metadata

    # Agency must be present AND not empty because we are accessing the first index
    is_agency_present = (
        dataset.agency is not None
        and AGENCY_TIMEZONE in dataset.agency.columns
        and not dataset.agency.empty
    )

    if is_agency_present:
        # Extract main timezone
        main_timezone = dataset.agency[AGENCY_TIMEZONE].iloc[AGENCY_TIMEZONE_IDX]
    else:
        main_timezone = ""

    stop_timezones = set()
    if dataset.stops is not None and STOP_TIMEZONE in dataset.stops.columns:
        # Extract the timezones using the stop_timezone in the dataset stops
        for index, row in dataset.stops.iterrows():
            if row[STOP_TIMEZONE] is not None:
                stop_timezones.add(row[STOP_TIMEZONE])

    # Remove the main_timezone from the set of the stop_timezones
    # to create the other_timezones
    other_timezones = []
    if len(stop_timezones) != 0:
        other_timezones = stop_timezones
        other_timezones.discard(main_timezone)
        # Convert the set of time to a list, and sort it alphabetically
        other_timezones = sorted(list(other_timezones))

    # Set the timezones in the GTFS representation
    metadata.main_timezone = main_timezone
    metadata.other_timezones = other_timezones

    return gtfs_representation
