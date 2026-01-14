import os
import argparse
from dedupe import config, registry


class RegistryTest:
    test_db = "testing.sqlite"

    def setup_class(self):
        # Don't update a main registry
        config.GLOBAL_REGISTRY = RegistryTest.test_db


    def teardown_class(self):
        os.remove(config.GLOBAL_REGISTRY)


    def dump_registry(self):
        args = argparse.Namespace(path=r"%all")
        registry.get_hash(args)