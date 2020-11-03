from hashlib import md5


class ProcessMd5:
    def __init__(self, datasets, md5_hashes):
        """Constructor for ``ProcessMd5``.
        :param datasets: The datasets for which to process MD5 hash verification. The `datasets` must be a dictionary,
        where a key is an entity code and a value is a path to a dataset zip file.
        :param md5_hashes: The MD5 hashes of the datasets versions in the database. The `md5_hashes` must be
        a dictionary, where a key is an entity code and a value is a set of the MD5 hashes associated
        to the datasets versions to the entity code.
        """
        try:
            if datasets is None or not isinstance(datasets, dict):
                raise TypeError("Datasets must be a valid dictionary.")
            self.datasets = datasets
            if md5_hashes is None or not isinstance(md5_hashes, dict):
                raise TypeError("MD5 hashes must be a valid dictionary.")
            self.md5_hashes = md5_hashes
        except Exception as e:
            raise e

    def execute(self):
        """Execute the ``ProcessMd5`` use case.
        :return: The datasets for which the MD5 hashes are not in the database.
        N.B.: a dataset for which the MD5 hash is not in the database represents a new dataset version.
        """
        entity_codes = list(self.datasets.keys())

        for entity_code in entity_codes:
            md5_hash = md5()
            dataset_file = self.datasets[entity_code]
            try:
                print("--------------- Processing MD5 : %s ---------------\n" % dataset_file)
                with open(dataset_file, "rb") as f:
                    while data := f.read(4096):
                        md5_hash.update(data)

                if md5_hash not in self.md5_hashes[entity_code]:
                    print("Success : new MD5 hash %s for %s, dataset kept for further processing\n" %
                          (md5_hash.hexdigest(), dataset_file))
                else:
                    del self.datasets[entity_code]
                    print("Success : MD5 hash %s already exists for %s, dataset discarded\n" %
                          (md5_hash.hexdigest(), dataset_file))
            except Exception as e:
                print("Exception \"%s\" occurred when processing MD5 hash\n" % e)

        return self.datasets
