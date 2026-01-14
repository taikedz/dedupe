import os
from dedupe import registry

class RegistryTest:
    test_db = "testing.sqlite"

    def setup_class(self):
        # Don't update a main registry
        registry.GLOBAL_REGISTRY = RegistryTest.test_db


    def teardown_class(self):
        os.remove(registry.GLOBAL_REGISTRY)