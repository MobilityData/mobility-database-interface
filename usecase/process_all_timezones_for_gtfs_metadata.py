from representation.gtfs_representation import GtfsRepresentation


class ProcessAllTimezonesForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessAllTimezonesForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessAllTimezonesForGtfsMetadata`` use case.
        Process all the timezones using the`stops` file from the GTFS dataset of the representation.
        Add the list of all the timezones to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the all the timezones using the stop_timezone in the dataset stops
        all_timezones = set()
        if 'stop_timezone' in dataset.stops.columns:
            for index, row in dataset.stops.iterrows():
                if row['stop_timezone'] is not None:
                    all_timezones.add(row['stop_timezone'])

        # Extract the timezone from the first row in the dataset agency
        # if the set of all timezones is empty after processing the dataset stops
        if len(all_timezones) == 0:
            all_timezones.add(dataset.agency['agency_timezone'].iloc[0])

        self.gtfs_representation.set_metadata_all_timezones(sorted(list(all_timezones)))
        return self.gtfs_representation
