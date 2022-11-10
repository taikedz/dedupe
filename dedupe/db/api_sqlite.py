import sqlite3

from dedupe.db.api_generic import DbApiGeneric

class SQLiteApi(DbApiGeneric):
    
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)


    def __destroy__(self):
        self.db.close()


    def _query(self, query, values):
        with self.db.cursor() as c:
            res = c.execute(query, values)
            self.db.commit()
        return res


    def add_path(self, path, size, short_hash='', full_hash=''):
        self._query("INSERT into Entries(path,size,short_hash,full_hash) VALUES (?,?,?,?)",
            (path,size,short_hash,full_hash))


    def delete_path(self, path):
        self._query("DELETE FROM Entries WHERE path=?", (path,))


    def update_path(self, path, size=None, short_hash=None, full_hash=None):

        self._query("UPDATE Entries SET(size=?,short_hash=?,full_hash=?)",
            (size,short_hash,full_hash))


    def get_path_info(self, path):
        res = self._query("SELECT size,short_hash,full_hash FROM Entries WHERE path=?", (path,))
        return res # FIXME - we probably need to unpack the data a little


    def find_path_duplicates(self, path):
        raise NotImplementedError()


    def find_hash_duplicates(self, full_hash):
        raise NotImplementedError()
