
from typing import Tuple
from dataclasses import dataclass


class DedupeDatabaseError(Exception): pass

@dataclass
class FieldDef:
    name: str
    dtype: str
    index: bool = False
    primary: bool = False
    foreign_key: Tuple[str,str] = None, # foreign table, foreign name

class FieldDefError(Exception): pass

class DbApiGeneric:
    """ Generic Database API class.

    Subclass this to implement a target database library/engine (see api_sqlite.py for an example)

    This class provides genericised table definitions, so that implementing classes
    can perform a suitable data type conversion. For example "text" can be a SQLite "TEXT"
    type, whereas in MySQL it would be represented by a "BLOB" type perhaps.
    """

    PATHS_TABLE = [
        FieldDef("path", "chars:256", True, True),
        FieldDef("size", "int"),
        FieldDef("short_hash", "chars:64"),
        FieldDef("full_hash", "chars:64"),
    ]

    DUPLICATES_TABLE = [
        FieldDef("full_hash", "chars:64", True, True, ("Paths", "full_hash"))
    ]


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

        self.create_table("Paths", self.PATHS_TABLE)
        self.create_table("Duplicates", self.DUPLICATES_TABLE)


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


    def get_path_info(self, path):
        raise NotImplementedError()


    def find_path_duplicates(self, path):
        raise NotImplementedError()


    def find_hash_duplicates(self, full_hash):
        raise NotImplementedError()
