from representation.gtfs_representation import GtfsRepresentation


class ProcessMainLanguageCodeForGtfsMetadata:
    def __init__(self, gtfs_representation):
        """Constructor for ``ProcessMainLanguageCodeForGtfsMetadata``.
        :param gtfs_representation: The representation of the GTFS dataset to process.
        """
        try:
            if gtfs_representation is None or not isinstance(gtfs_representation, GtfsRepresentation):
                raise TypeError("GTFS data representation must be a valid GtfsRepresentation.")
            self.gtfs_representation = gtfs_representation
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessMainLanguageCodeForGtfsMetadata`` use case.
        Process the main language code using the`agency` file from the GTFS dataset of the representation.
        Add the main language code to the representation metadata once processed.
        :return: The representation of the GTFS dataset post-execution.
        """
        dataset = self.gtfs_representation.get_dataset()

        # Extract the main language code from the first row in the dataset agency
        main_language_code = dataset.agency['agency_lang'].iloc[0]

        self.gtfs_representation.set_metadata_main_language_code(main_language_code)
        return self.gtfs_representation
