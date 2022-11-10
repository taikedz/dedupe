import sqlite3
from typing import List

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
    
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)

        DbApiGeneric.__init__(self)


    def __destroy__(self):
        self.db.close()


    def create_table(self, table_name:str, table_def:List[FieldDef]):
        field_queries = []

        # First build fields-proper
        for field in table_def:
            subq = []
            subq.append(f"{field.name} {get_field_type(field.dtype)}")

            if field.index:
                subq.append("INDEX")
            if field.primary:
                subq.append("PRIMARY KEY")

            field_queries.append(" ".join(subq))

        # Add foreign key definitions at the end
        for field in table_def:
            if field.foreign_key:
                field_queries.append(f"FOREIGN KEY ({field.name} REFERENCES {field.foreign_key[0]} ({field.foreign_key[1]}))")

        query = f"""
        CREATE TABLE {table_name} (
            {",\n".join(field_queries)}
        )
        """

        self._query(query)


    def _query(self, query, *values):
        c = None
        try:
            c = self.db.cursor()
            res = c.execute(query, *values)
            self.db.commit()
        except:
            if c != None:
                c.close()
            raise
        return res


    def add_path(self, path, size, short_hash='', full_hash=''):
        self._query("INSERT into Entries(path,size,short_hash,full_hash) VALUES (?,?,?,?)",
            (path,size,short_hash,full_hash))


    def delete_path(self, path):
        self._query("DELETE FROM Entries WHERE path=?", (path,))


    def update_path(self, path, size=None, short_hash=None, full_hash=None):
        info = self.get_path_info(path)

        if size is None: size = info["size"]
        if short_hash is None: short_hash = info["short_hash"]
        if full_hash is None: full_hash = info["full_hash"]

        self._query("UPDATE Entries SET(size=?,short_hash=?,full_hash=?)",
            (str(size),short_hash,full_hash))


    def get_path_info(self, path):
        properties = ["size","short_hash","full_hash"]
        res = self._query(f"SELECT {','.join(properties)} FROM Entries WHERE path=?", (path,))
        entries = [r for r in res]

        if len(entries) != 1:
            # Not likely to be more than 1, could be zero.
            raise DedupeDatabaseError(f"Entry not found for {path}: {entries}")

        info = {k:v for k,v in zip(properties, entries[0])}
        info["size"] = int(info["size"])

        return info


    def find_path_duplicates(self, path):
        raise NotImplementedError()


    def find_hash_duplicates(self, full_hash):
        raise NotImplementedError()
