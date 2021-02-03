from hashlib import md5

DATA_CHUNK_BYTE_SIZE = 4096
PATH_TO_DATASET_KEY = "path"
MD5_HASH_KEY = "md5"


def process_md5(paths_to_datasets, previous_md5_hashes):
    """Computes the MD5 hash of the datasets. Removes the datasets for which the MD5 hash is already in the database.
    N.B.: a dataset for which the MD5 hash is not in the database represents a new dataset version.
    :param paths_to_datasets: The datasets for which to process MD5 hash verification. The `datasets` must be
    a dictionary, where a key is an entity code and a value is a path to a dataset zip file.
    :param previous_md5_hashes: The MD5 hashes of the datasets versions in the database. The `md5_hashes` must be
    a dictionary, where a key is an entity code and a value is a set of the MD5 hashes associated
    to the datasets versions to the entity code.
    :return: The datasets for which the MD5 hashes are not in the database. These updated datasets are returned in a
    dictionary, where a key is an entity code and a value is a sub-dictionary including a path to a dataset zip file
    and the new MD5 hash processed.
    """
    if not isinstance(paths_to_datasets, dict):
        raise TypeError("Datasets must be a valid dictionary.")
    if not isinstance(previous_md5_hashes, dict):
        raise TypeError("MD5 hashes must be a valid dictionary.")
    if paths_to_datasets.keys() != previous_md5_hashes.keys():
        raise Exception("Datasets and MD5 hashes dictionaries must share the same keys (entity codes).")
    entity_codes = list(paths_to_datasets.keys())
    paths_to_datasets_and_md5 = {}

    for entity_code in entity_codes:
        md5_hash = md5()
        path_to_dataset = paths_to_datasets[entity_code]
        previous_md5_hash = previous_md5_hashes[entity_code]

        print(f"--------------- Processing MD5 : {path_to_dataset} ---------------\n")
        try:
            with open(path_to_dataset, "rb") as f:
                while data := f.read(DATA_CHUNK_BYTE_SIZE):
                    md5_hash.update(data)
        except OSError:
            print("OSError occurred when processing MD5 hash: could not open or read file.\n")

        md5_hash = md5_hash.hexdigest()
        if md5_hash not in previous_md5_hash:
            paths_to_datasets_and_md5[entity_code] = {PATH_TO_DATASET_KEY: path_to_dataset, MD5_HASH_KEY: md5_hash}
            print(f"Success : new MD5 hash {md5_hash} for {path_to_dataset}, dataset kept for further processing\n")
        else:
            print(f"Success : MD5 hash {md5_hash} already exists for {path_to_dataset}, dataset discarded\n")

    return paths_to_datasets_and_md5

