import os
import argparse
import unittest # lib, not current dir
import shutil
from pathlib import Path

from dedupe import config, registry, fs


class RegistryTest(unittest.TestCase):
    test_db = "testing.sqlite"

    def __init__(self, *a, **kw):
        unittest.TestCase.__init__(self, *a, **kw)

    def setup_class(self):
        # Don't update a main registry
        config.GLOBAL_REGISTRY = RegistryTest.test_db


    def teardown_class(self):
        os.remove(config.GLOBAL_REGISTRY)


    def dump_registry(self):
        # TODO - get as strings and return
        args = argparse.Namespace(path=r"%all")
        registry.get_hash(args)


class FileSet:
    def __init__(self, holddir:str, files:dict[str,str]):
        self._hdir = Path(holddir)
        self._fileset = files


    def __enter__(self):
        self.make_files()
        return self
    

    def __exit__(self, *e):
        self.delete_files()


    def make_files(self):
        for path,data in self._fileset.items():
            path = self._hdir/path
            parent = path.parent
            os.makedirs(parent, exist_ok=True)
            with open(path, 'w') as fh:
                fh.write(data)


    def delete_files(self):
        shutil.rmtree(self._hdir)


    def all_files(self) -> list[str]:
        return fs.all_files(self._hdir)
