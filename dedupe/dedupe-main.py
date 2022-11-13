import os
import unittest
import dedupe.db
from dedupe.hash import hash_file

# 4 MiB
SHORT_HASH_MAX_BYTES = 1024 * 1024 * 4

# The main duplicates database file
# FIXME - make the file name configurable
DB = dedupe.db.connect_sqlite("Duplicates.db")


def get_byte_size(path):
    return os.stat(path).st_size


def register_path(main_path:str) -> bool:
    """ Register a new file path

    :param main_path: the path to the target file

    :return: whether duplicates were found when adding the path
    """
    size = get_byte_size(main_path)

    # ------- First, check for size duplicates
    files = DB.lookup("size", size)
    # Add our new path afterwards
    DB.add_path(main_path, size=size)
    if not files: return False

    # ------- Size duplicates found, generate short hashes
    _shorthash = lambda _p: hash_file(_p, max_bytes=SHORT_HASH_MAX_BYTES)

    main_short_hash = _shorthash(main_path)
    __update_hashes(files, "short_hash", _shorthash)

    # ------- Check for short hash duplicates
    files = DB.lookup("short_hash", main_short_hash)
    # Add our shorthas afterwards
    DB.update_path(main_path, short_hash=main_short_hash)
    if not files: return False

    # ------- Short hash duplicates found,  generate full hashes
    main_full_hash = hash_file(main_path)
    __update_hashes(files, "full_hash", hash_file)

    files = DB.lookup("full_hash", main_full_hash)
    DB.update_path(main_path, full_hash=main_full_hash)
    if not files: return False

    DB.register_duplicate(main_full_hash)

    return True


def __update_hashes(files, field_name, operation):
    for f in files:
        if f[field_name] == '':
            path = f["path"]
            DB.update_path(path, **{field_name: operation(path)})


# ==========================================

class DedupeAlgorithmTest(unittest.TestCase):
    base_name = "local_test"
    names_data = {
        "one":"one and all",
        "uno":"one and all",
        "eins":"stuff",
        "two":"ane and all",
    }

    @classmethod
    def setUpClass(cls) -> None:
        for name, data in cls.names_data.items():
            with open(f"{cls.base_name}_{name}.txt", 'w') as fh:
                fh.write(data)

    @classmethod
    def tearDownClass(cls) -> None:
        [os.remove(f"{cls.base_name}_{name}.txt") for name in cls.names_data.keys()]


    def test_duplicates(self):
        """ Check that duplicates are identified, and short/full hashes are only
        generated when necessary
        """
        # Make the short has max be small enough so as to
        #  cause distinct short and long hashes
        global SHORT_HASH_MAX_BYTES
        SHORT_HASH_MAX_BYTES=4

        # First entry, no duplicates possible
        assert not register_path(f"{self.base_name}_one.txt")
        assert not DB.get_path_info(f"{self.base_name}_one.txt")["short_hash"]

        # uno is same as one - should be found, and generate short and full hashes
        assert register_path(f"{self.base_name}_uno.txt")

        one_pi = DB.get_path_info(f"{self.base_name}_one.txt")
        uno_pi = DB.get_path_info(f"{self.base_name}_uno.txt")

        assert DB.find_hash_duplicates(one_pi["full_hash"]) == ['local_test_one.txt', 'local_test_uno.txt']

        assert one_pi["full_hash"]
        assert one_pi["short_hash"]
        assert uno_pi["full_hash"]
        assert uno_pi["short_hash"]

        assert (one_pi["full_hash"] != one_pi["short_hash"])

        # Different length causes no hashes
        assert not register_path(f"{self.base_name}_eins.txt")
        assert not DB.get_path_info(f"{self.base_name}_eins.txt")["short_hash"]
        assert not DB.get_path_info(f"{self.base_name}_eins.txt")["full_hash"]

        # Same length, different start data causes short hash but not full
        assert not register_path(f"{self.base_name}_two.txt")

        two_pi = DB.get_path_info(f"{self.base_name}_two.txt")
        assert one_pi["size"] == two_pi["size"]
        assert one_pi["short_hash"] != two_pi["short_hash"]
        assert not two_pi["full_hash"]

        assert DB.get_registered_duplicates() == [one_pi["full_hash"]]
