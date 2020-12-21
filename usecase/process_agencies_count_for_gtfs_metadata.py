from representation.gtfs_representation import GtfsRepresentation


class ProcessAgenciesCountForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessAgenciesCountByTypeForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessAgenciesCountByTypeForGtfsMetadata`` use case.
        Process and count all the agencies in the `agency` file from the GTFS dataset of the representation.
        Add the agencies count to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Count agencies
        agencies_count = dataset.agency['agency_id'].size

        self.gtfs_representation.set_metadata_agencies_count(agencies_count)
        return self.gtfs_representation
