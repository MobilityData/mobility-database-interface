from representation.gtfs_representation import GtfsRepresentation


class ProcessMainTimezoneForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessMainTimezoneForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessMainTimezoneForGtfsMetadata`` use case.
        Process the main timezone using the`agency` file from the GTFS dataset of the representation.
        Add the main timezone to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the main timezone from the first row in the dataset agency
        main_timezone = dataset.agency['agency_timezone'].iloc[0]

        self.gtfs_representation.set_metadata_main_timezone(main_timezone)
        return self.gtfs_representation
