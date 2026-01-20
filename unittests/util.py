import os
import argparse
import unittest # lib, not current dir
from dedupe import config, registry


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
