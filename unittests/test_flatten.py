from dedupe import flatten
from unittests.makefiles import FileSet
from unittests.util import RegistryTest


class TestFlatten(RegistryTest):

    def testFlatten(self):
        fileset = {
            "readme.txt": "hi",
            "license.txt": "gpl",
            "old-src/name.c": "alice",
            "old-src/readme.txt": "hi",
            "old-src/version/v.c": "ZERO",
            "src/name.c": "bob",
            "src/version.c": "zero",
        }

        with FileSet("testing", fileset) as fs:
            flatten.flatten("testing")

            assert fs.all_files() ==  [
                "testing/license.txt",
                "testing/name.c",
                "testing/name.c-1",
                "testing/old-src/readme.txt",
                "testing/readme.txt",
                "testing/v.c",
                "testing/version.c",
            ]