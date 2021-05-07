from hashlib import sha1

from representation.dataset_infos import DatasetInfos

DATA_CHUNK_BYTE_SIZE = 4096


def process_sha1(dataset_infos):
    """Computes the SHA-1 hash of the datasets. Removes the datasets for which the SHA-1 hash is already in the database.
    N.B.: a dataset for which the SHA-1 hash is not in the database represents a new dataset version.
    :param datasets_infos: A list of DatasetInfos containing to path to the dataset needing a SHA-1 hash verification,
    and the previous SHA-1 hashes.
    :return: A list of DatasetInfos for which the SHA-1 hashes are not in the database.
    """
    if not isinstance(dataset_infos, DatasetInfos):
        raise TypeError("Datasets infos must be a valid DatasetInfos list.")

    sha1_hash = sha1()
    path_to_dataset = dataset_infos.zip_path
    previous_sha1_hashes = dataset_infos.previous_sha1_hashes

    print(f"--------------- Processing SHA-1 : {path_to_dataset} ---------------\n")
    try:
        with open(path_to_dataset, "rb") as f:
            while data := f.read(DATA_CHUNK_BYTE_SIZE):
                sha1_hash.update(data)
    except OSError:
        print(
            "OSError occurred when processing SHA-1 hash: could not open or read file.\n"
        )

    sha1_hash = sha1_hash.hexdigest()
    if sha1_hash not in previous_sha1_hashes:
        dataset_infos.sha1_hash = sha1_hash
        print(
            f"Success : new SHA-1 hash {sha1_hash} for {path_to_dataset}, dataset kept for further processing\n"
        )
    else:
        print(
            f"SHA-1 hash {sha1_hash} already exists for {path_to_dataset}, dataset discarded\n"
        )

    return dataset_infos
