
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

from dedupe.errors import DedupeError
from dedupe.hash import hash_file


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


    def __init__(self, short_hash_max_bytes:int=None):
        """ Override and callback this method:

        Open a connection to your database first, then call this super-class constructor

        e.g.

        ```python
        def __init__(self, **db_details):
            # Do this first
            dbengine.connect(**db_details)

            DbApiGeneric.__init__(self)
        ```
        """
        if type(self) == DbApiGeneric:
            raise NotImplementedError("Cannot call init of DbApiGeneric. Please instantiate from a subclass.")

        self.create_table(self.PATHS_TABLE_NAME, self.PATHS_TABLE)
        self.create_table(self.DUPLICATES_TABLE_NAME, self.DUPLICATES_TABLE)

        self.short_bytes_max = (
            short_hash_max_bytes if short_hash_max_bytes
                else 1024*1024*4) # 4 MiB


    def __update_hashes(self, files, field_name, operation):
        for f in files:
            if f[field_name] == '':
                path = f["path"]
                self.update_path(path, **{field_name: operation(path)})


    def register_path(self, main_path:str) -> bool:
        """ Register a new file path

        :param main_path: the path to the target file

        :return: whether duplicates were found when adding the path
        """
        size = os.stat(main_path).st_size

        # ------- First, check for size duplicates
        files = self.lookup("size", size)
        # Add our new path afterwards
        self.add_path(main_path, size=size)
        if not files: return False

        # ------- Size duplicates found, generate short hashes
        _shorthash = lambda _p: hash_file(_p, max_bytes=self.short_bytes_max)

        main_short_hash = _shorthash(main_path)
        self.__update_hashes(files, "short_hash", _shorthash)

        # ------- Check for short hash duplicates
        files = self.lookup("short_hash", main_short_hash)
        # Add our shorthas afterwards
        self.update_path(main_path, short_hash=main_short_hash)
        if not files: return False

        # ------- Short hash duplicates found,  generate full hashes
        main_full_hash = hash_file(main_path)
        self.__update_hashes(files, "full_hash", hash_file)

        files = self.lookup("full_hash", main_full_hash)
        self.update_path(main_path, full_hash=main_full_hash)
        if not files: return False

        self.register_duplicate(main_full_hash)

        return True


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
