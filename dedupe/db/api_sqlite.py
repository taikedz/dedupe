import sqlite3
from typing import Dict, List

from dedupe.db.api_generic import DbApiGeneric, DedupeDatabaseError, FieldDef, FieldDefError

TYPES = {
    # Workaround: Implementing 'int' type as TEXT to preserve ginormous numbers
    "int": "TEXT",
    "chars": "TEXT"
}

def get_field_type(type_spec:str):
    """ Convert unified notation/type into engine's type
    """
    parts = type_spec.split(":")

    if len(parts) <= 0:
        raise FieldDefError(f"Empty definition {type_spec}")

    else:
        return TYPES[parts[0]]


class SQLiteApi(DbApiGeneric):
    
    def __init__(self, db_path:str):
        self.db = sqlite3.connect(db_path)

        DbApiGeneric.__init__(self)


    def __destroy__(self):
        self.db.close()


    def _table_exists(self, table_name:str) -> bool:
        query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{table_name}';"
        table_list = [r[0] for r in self._query(query)]
        return bool(table_list)


    def create_table(self, table_name:str, table_def:List[FieldDef]):
        if self._table_exists(table_name):
            print(f"Table {table_name} exists, re-using.")
            return
        else:
            print(f"Creating table {table_name}")

        field_queries = []

        # First build fields-proper
        for field in table_def:
            subq = []
            subq.append(f"{field.name} {get_field_type(field.dtype)}")

            if field.primary:
                subq.append("PRIMARY KEY")

            field_queries.append(" ".join(subq))

        # Add foreign key definitions at the end
        for field in table_def:
            if field.foreign_key:
                field_queries.append(f"FOREIGN KEY ({field.name}) REFERENCES {field.foreign_key[0]} ({field.foreign_key[1]})")

        index_fields = [f.name for f in table_def if f.index]
        index_query = None
        if index_fields:
            index_name = "idx_"+"_".join(index_fields)
            index_query = f"CREATE INDEX {index_name} ON {table_name} ({','.join(index_fields)})"

        joined_field_queries = ",\n".join(field_queries)
        table_query = f"""
        CREATE TABLE {table_name} (
            {joined_field_queries}
        );
        """

        self._query(table_query)
        if index_query:
            self._query(index_query)
        
        print("-- Created.")


    def _query(self, query:str, *values) -> List[Dict]:
        c = None
        try:
            c = self.db.cursor()
            res = c.execute(query, *values)
            self.db.commit()
        except:
            if c != None:
                c.close()
            raise
        return [d for d in res]


    def add_path(self, path:str, size:int, short_hash:str='', full_hash:str=''):
        self._query(f"INSERT into {self.PATHS_TABLE_NAME}(path,size,short_hash,full_hash) VALUES (?,?,?,?)",
            (path,size,short_hash,full_hash))


    def delete_path(self, path:str):
        self._query(f"DELETE FROM {self.PATHS_TABLE_NAME} WHERE path=?", (path,))


    def update_path(self, path:str, size:int=None, short_hash:str=None, full_hash:str=None):
        info = self.get_path_info(path)

        if size is None: size = info["size"]
        if short_hash is None: short_hash = info["short_hash"]
        if full_hash is None: full_hash = info["full_hash"]

        self._query(f"UPDATE {self.PATHS_TABLE_NAME} SET size=?,short_hash=?,full_hash=? WHERE path=?",
            (str(size),short_hash,full_hash, path))


    def get_path_info(self, path:str) -> Dict:
        properties = ["size","short_hash","full_hash"]
        res = self._query(f"SELECT {','.join(properties)} FROM {self.PATHS_TABLE_NAME} WHERE path=?", (path,))
        entries = [r for r in res]

        if len(entries) != 1:
            # Not likely to be more than 1, could be zero.
            raise DedupeDatabaseError(f"Single entry not found for {path}: {entries}")

        info = {k:v for k,v in zip(properties, entries[0])}
        info["size"] = int(info["size"])

        return info


    def find_path_duplicates(self, path:str) -> List[Dict]:
        qres = self.get_path_info(path)
        return self.find_hash_duplicates(qres["full_hash"])


    def find_hash_duplicates(self, full_hash) -> List[Dict]:
        qres = self._query(f"SELECT path FROM {self.PATHS_TABLE_NAME} WHERE full_hash=?", (full_hash,))
        return [d[0] for d in qres]


if __name__ == "__main__":
    def _info_matches(path, data):
        try:
            obtained = api.get_path_info(path)
            assert data == obtained, f"Data mismtach {data} != {obtained}"
        except DedupeDatabaseError:
            assert data is None, f"Should have got data for {path}, but got nothing"

    api = SQLiteApi("here.db")
    api.add_path("/a", 128)
    api.add_path("/b", 128)
    _info_matches("/a", {'size':128, 'short_hash':'', 'full_hash': ''})

    api.update_path("/a", short_hash="asdfg")
    _info_matches("/a", {'size':128, 'short_hash':'asdfg', 'full_hash': ''})
    _info_matches("/b", {'size':128, 'short_hash':'', 'full_hash': ''})

    api.update_path("/a", full_hash="dupe")
    api.update_path("/b", full_hash="dupe")
    assert api.find_path_duplicates("/a") == ["/a", "/b"]
    assert api.find_hash_duplicates("dupe") == ["/a", "/b"], api.find_hash_duplicates("dupe")

    api.delete_path("/a")
    _info_matches("/a", None)
    _info_matches("/b", {'size':128, 'short_hash':'', 'full_hash': 'dupe'})

    try:
        api.add_path("/b", 128)
        assert False, "Expected failure, but passed.dupe"
    except sqlite3.IntegrityError:
        pass

    print("Basic tests passed")
