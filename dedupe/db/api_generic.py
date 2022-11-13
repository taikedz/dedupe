
from typing import Dict, List, Tuple
from dataclasses import dataclass

from dedupe.errors import DedupeError


class DedupeDatabaseError(DedupeError): pass

@dataclass
class FieldDef:
    name: str
    dtype: str
    index: bool = False
    primary: bool = False
    foreign_key: Tuple[str,str] = None # foreign table, foreign name

class FieldDefError(DedupeError): pass

class DbApiGeneric:
    """ Generic Database API class.

    Subclass this to implement a target database library/engine (see api_sqlite.py for an example)

    This class provides genericised table definitions, so that implementing classes
    can perform a suitable data type conversion. For example "chars:128" can be a SQLite "TEXT"
    type, whereas in MySQL it would be represented by a "VARCHAR[128]" type (or any other).
    """

    PATHS_TABLE = [
        FieldDef("path", "chars:256", True, True),
        FieldDef("size", "int", index=True),
        FieldDef("short_hash", "chars:64", index=True),
        FieldDef("full_hash", "chars:64", index=True),
    ]

    DUPLICATES_TABLE = [
        FieldDef("full_hash", "chars:64", True, True, ("Paths", "full_hash"))
    ]

    PATHS_TABLE_NAME = "Paths"
    DUPLICATES_TABLE_NAME = "Duplicates"


    def __init__(self):
        """ Override this method.

        Open a connection to your database first, then call this super-class constructor

        e.g.

        ```python
        def __init__(self, **db_details):
            # Do this first
            dbengine.connect(**dbdetails)

            DbApiGeneric.__init__(self)
        ```
        """
        if type(self) == DbApiGeneric:
            raise NotImplementedError("Cannot call init of DbApiGeneric. Please instantiate from a subclass.")

        self.create_table(self.PATHS_TABLE_NAME, self.PATHS_TABLE)
        self.create_table(self.DUPLICATES_TABLE_NAME, self.DUPLICATES_TABLE)


    # ==============================
    # 'Abstract' placeholder methods

    def create_table(self, table_name:str, table_def:FieldDef):
        raise NotImplementedError()


    def add_path(self, path, size, short_hash, full_hash):
        raise NotImplementedError()


    def delete_path(self, path):
        raise NotImplementedError()


    def update_path(self, path, size, short_hash, full_hash):
        raise NotImplementedError()


    def get_path_info(self, path) -> Dict:
        raise NotImplementedError()


    def register_duplicate(self, full_hash):
        raise NotImplementedError()


    def get_registered_duplicates(self) -> List[str]:
        raise NotImplementedError()


    def lookup(self, property, value) -> List[Dict]:
        raise NotImplementedError()


    def find_path_duplicates(self, path) -> List[Dict]:
        raise NotImplementedError()


    def find_hash_duplicates(self, full_hash) -> List[Dict]:
        raise NotImplementedError()
