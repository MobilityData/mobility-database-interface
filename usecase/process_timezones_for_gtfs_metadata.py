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
    agency_is_present = (
        dataset.agency is not None
        and AGENCY_TIMEZONE in dataset.agency.columns
        and not dataset.agency.empty
    )
    stops_are_present = (
        dataset.stops is not None and STOP_TIMEZONE in dataset.stops.columns
    )

    if agency_is_present or stops_are_present:
        if agency_is_present:
            # Extract main timezone
            main_timezone = dataset.agency[AGENCY_TIMEZONE].iloc[AGENCY_TIMEZONE_IDX]
        else:
            main_timezone = ""

        stop_timezones = set()
        if stops_are_present:
            # Extract the timezones using the stop_timezone in the dataset stops
            for index, row in dataset.stops.iterrows():
                # Keep the stop timezone only if the value exist and is not empty
                if row[STOP_TIMEZONE] is not None and len(row[STOP_TIMEZONE]) != 0:
                    stop_timezones.add(row[STOP_TIMEZONE])

        # Remove the main_timezone from the set of the stop_timezones
        # to create the other_timezones
        other_timezones = set()
        if len(stop_timezones) != 0:
            other_timezones.update(stop_timezones)
            other_timezones.discard(main_timezone)
            # Convert the set of time to a list, and sort it alphabetically
            other_timezones = sorted(list(other_timezones))

        # Set the timezones in the GTFS representation
        # if they are not empty
        if len(main_timezone) != 0:
            metadata.main_timezone = main_timezone
        if len(other_timezones) != 0:
            metadata.other_timezones = other_timezones

    return gtfs_representation
