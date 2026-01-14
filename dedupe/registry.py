import os
import pathlib
import sqlite3

from dedupe import config, ignore
import dedupe.hashutil as hashutil


class HashRegistry:
    def __init__(self, filepath=None, temp=False):
        if filepath is None:
            filepath = config.GLOBAL_REGISTRY
        os.makedirs(pathlib.Path(filepath).parent, exist_ok=True)

        self._path = filepath
        self._db = None
        self._cursor = None
        self._temp = temp


    def __enter__(self):
        self.open()
        return self


    def __exit__(self, *e):
        self.close()
        if self._temp:
            os.remove(self._path)


    def close(self):
        self._db.commit()
        self._db.close()
    

    def open(self):
        self._db = sqlite3.connect(self._path)
        self._cursor = self._db.cursor()
        res = [x for x in self._cursor.execute("SELECT * FROM sqlite_master WHERE type=? AND name=?", ("table", "HashedFiles"))]
        if not res:
            self._cursor.execute("CREATE TABLE HashedFiles(path TEXT, shorthash TEXT, hash TEXT)")
            self._db.commit()


    def allEntries(self):
        return [x for x in self._cursor.execute("SELECT path,shorthash,hash FROM HashedFiles")]


    def hashForPath(self, path, add=False) -> tuple[str,str,str]:
        abspath = str(pathlib.Path(path).absolute())
        res = [x for x in self._cursor.execute("SELECT path,shorthash,hash FROM HashedFiles WHERE path=?", (abspath,)) ]
        assert len(res) <= 1, f"Hash list for single path should have no more than one. Found: {res}"
        if res:
            return res[0]
        else:
            if not add:
                return None
            self.addFile(path)
            return self.hashForPath(path, add=False)


    def addFile(self, path):
        if ignore.should_ignore(path):
            return

        path = str(pathlib.Path(path).absolute())

        new_short_hash = hashutil.shortHash(path)
        existing_files = [x for x in self._cursor.execute("SELECT rowid,path,hash FROM HashedFiles WHERE shorthash=?", (new_short_hash,)) ]

        if existing_files:
            if path in [p for _r,p,_h in existing_files]:
                return
            for rowid,ef_path, longhash in existing_files:
                if longhash == '':
                    if pathlib.Path(ef_path).exists():
                        new_hash = hashutil.fullHash(ef_path)
                        self._cursor.execute("UPDATE HashedFiles SET hash=? WHERE rowid=?", (new_hash, rowid))
                    else:
                        # disappeared since
                        self.dropFile(ef_path)

            self._cursor.execute("INSERT INTO HashedFiles VALUES (?, ?, ?)", (path, new_short_hash, hashutil.fullHash(path)))
        else:
            self._cursor.execute("INSERT INTO HashedFiles VALUES (?, ?, ?)", (path, new_short_hash, ''))

        self._db.commit()


    def registerDir(self, path):
        for parentDir, folders, files in os.walk(path):
            for f in files:
                self.addFile(f"{parentDir}/{f}")

            dirscopy = folders[:]
            for d in dirscopy:
                if ignore.should_ignore(f"{parentDir}/{d}"):
                    folders.remove(d)


    def dropFile(self, abspath):
        self._cursor.execute("DELETE FROM HashedFiles WHERE path=?", (abspath,))
        self._db.commit()



def run(args):
    if args.path == r"%drop":
        os.remove(config.GLOBAL_REGISTRY)
        return
    
    with HashRegistry() as db:
        ppath = pathlib.Path(args.path)
        if ppath.is_dir():
            db.registerDir(args.path)
        elif ppath.is_file():
            db.addFile(args.path)
        else:
            raise ValueError(f"Could not process '{ppath.absolute()}'")


def get_hash(args):
    with HashRegistry() as db:
        if args.path == r"%all":
            entries = db.allEntries()
        else:
            entries = db.hashForPath(args.path)

        for p,s,h in entries:
            print(f"{p}\n  short={s}\n  full={h}")


# =======

def _demo():
    import sys
    import pprint

    with HashRegistry(sys.argv[1]) as db:
        db.registerDir(sys.argv[2])

        pprint.pprint(db.allEntries())


if __name__ == "__main__":
    _demo()