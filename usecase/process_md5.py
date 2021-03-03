from hashlib import md5
from utilities.validators import validate_datasets_infos

DATA_CHUNK_BYTE_SIZE = 4096


def process_md5(datasets_infos):
    """Computes the MD5 hash of the datasets. Removes the datasets for which the MD5 hash is already in the database.
    N.B.: a dataset for which the MD5 hash is not in the database represents a new dataset version.
    :param datasets_infos: A list of dataset infos containing to path to the dataset needing a MD5 hash verification,
    and the previous MD5 hashes.
    :return: The datasets infos of the datasets for which the MD5 hashes are not in the database.
    """
    validate_datasets_infos(datasets_infos)
    updated_datasets_infos = []

    # Decrementing the index to ensure no out of bound exception after the datasets_infos.pop(index)
    for dataset_infos in datasets_infos:
        md5_hash = md5()
        path_to_dataset = dataset_infos.zip_path
        previous_md5_hashes = dataset_infos.previous_md5_hashes

        print(f"--------------- Processing MD5 : {path_to_dataset} ---------------\n")
        try:
            with open(path_to_dataset, "rb") as f:
                while data := f.read(DATA_CHUNK_BYTE_SIZE):
                    md5_hash.update(data)
        except OSError:
            print(
                "OSError occurred when processing MD5 hash: could not open or read file.\n"
            )

        md5_hash = md5_hash.hexdigest()
        if md5_hash not in previous_md5_hashes:
            dataset_infos.md5_hash = md5_hash
            updated_datasets_infos.append(dataset_infos)
            print(
                f"Success : new MD5 hash {md5_hash} for {path_to_dataset}, dataset kept for further processing\n"
            )
        else:
            print(
                f"Success : MD5 hash {md5_hash} already exists for {path_to_dataset}, dataset discarded\n"
            )

    return updated_datasets_infos
