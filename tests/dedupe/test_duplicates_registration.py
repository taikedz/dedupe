import os
import unittest

from dedupe.db.api_generic import DbApiGeneric
from dedupe.db.api_sqlite import SQLiteApi
from tests.tempfs import TempFilesystem

class DedupeAlgorithmTest(unittest.TestCase):
    dir_name = "local_data/"

    file_content_data = """
    local_data:
        one.txt: one and all
        uno.txt: one and all
        eins.txt: stuff
        two.txt: ane and all
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.tempfs = TempFilesystem(cls.file_content_data)


    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempfs.cleanup()


    def setUp(self) -> None:
        # Make the short hash max be small enough so as to
        #  cause distinct short and long hashes
        self.DB:DbApiGeneric = SQLiteApi("duplicates.db", short_hash_max_bytes=4)


    def tearDown(self) -> None:
        os.remove("duplicates.db")


    def test_duplicates(self):
        """ Check that duplicates are identified, and short/full hashes are only
        generated when necessary
        """

        # First entry, no duplicates possible
        assert not self.DB.register_path(f"{self.dir_name}/one.txt")
        assert not self.DB.get_path_info(f"{self.dir_name}/one.txt")["short_hash"]

        # uno is same as one - should be found, and generate short and full hashes
        assert self.DB.register_path(f"{self.dir_name}/uno.txt")

        one_pi = self.DB.get_path_info(f"{self.dir_name}/one.txt")
        uno_pi = self.DB.get_path_info(f"{self.dir_name}/uno.txt")

        assert self.DB.find_hash_duplicates(one_pi["full_hash"]) == [
            f'{self.dir_name}/one.txt', f'{self.dir_name}/uno.txt']

        assert one_pi["full_hash"]
        assert one_pi["short_hash"]
        assert uno_pi["full_hash"]
        assert uno_pi["short_hash"]

        assert (one_pi["full_hash"] != one_pi["short_hash"])

        # Different length causes no hashes
        assert not self.DB.register_path(f"{self.dir_name}/eins.txt")
        assert not self.DB.get_path_info(f"{self.dir_name}/eins.txt")["short_hash"]
        assert not self.DB.get_path_info(f"{self.dir_name}/eins.txt")["full_hash"]

        # Same length, different start data causes short hash but not full
        assert not self.DB.register_path(f"{self.dir_name}/two.txt")

        two_pi = self.DB.get_path_info(f"{self.dir_name}/two.txt")
        assert one_pi["size"] == two_pi["size"]
        assert one_pi["short_hash"] != two_pi["short_hash"]
        assert not two_pi["full_hash"]

        assert self.DB.get_registered_duplicates() == [one_pi["full_hash"]]
