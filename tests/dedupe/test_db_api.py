
import os
import sqlite3
import unittest

from dedupe.db.api_generic import DedupeDatabaseError, DbApiGeneric
from dedupe.db.api_sqlite import SQLiteApi

# General test definition for all connectors
class GenericApi(unittest.TestCase):
    def execute_basic_verification(self, connector_method, *connector_params):
        print(f"Basic tests begin: {connector_method.__name__, connector_params}")

        def _info_matches(path, data):
            try:
                obtained = api.get_path_info(path)
                assert data == obtained, f"Data mismtach {data} != {obtained}"
            except DedupeDatabaseError:
                assert data is None, f"Should have got data for {path}, but got nothing"

        api:DbApiGeneric = connector_method(*connector_params)
        api.add_path("/a", 128)
        api.add_path("/b", 128)
        _info_matches("/a", {'path':'/a', 'size':128, 'short_hash':'', 'full_hash': ''})

        api.update_path("/a", short_hash="asdfg")
        _info_matches("/a", {'path':'/a', 'size':128, 'short_hash':'asdfg', 'full_hash': ''})
        _info_matches("/b", {'path':'/b', 'size':128, 'short_hash':'', 'full_hash': ''})

        api.update_path("/a", full_hash="dupe")
        api.update_path("/b", full_hash="dupe")
        assert api.find_path_duplicates("/a") == ["/a", "/b"]
        assert api.find_hash_duplicates("dupe") == ["/a", "/b"], api.find_hash_duplicates("dupe")

        api.delete_path("/a")
        _info_matches("/a", None)
        _info_matches("/b", {'path':'/b', 'size':128, 'short_hash':'', 'full_hash': 'dupe'})

        try:
            api.add_path("/b", 128)
            assert False, "Expected failure, but passed."
        except sqlite3.IntegrityError:
            pass

        api.register_duplicate("abc")
        api.register_duplicate("def")
        assert api.get_registered_duplicates() == ["abc", "def"]

        print(f"Basic tests passed: {connector_method.__name__, connector_params}")

# ===================
# Run the test against any available connectors

class TestSqliteApi(GenericApi):
    def test_sqlite(self):
        self.execute_basic_verification(SQLiteApi, "api_test.db")
        os.remove("api_test.db")