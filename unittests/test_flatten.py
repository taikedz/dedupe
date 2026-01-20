from dedupe import flatten
from unittests.util import RegistryTest, FileSet


class TestFlatten(RegistryTest):

    def testFlatten(self):
        fileset = {
            "readme.txt": "hi",
            "license.txt": "gpl",
            "version-link.c ->": "src/version.c",
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
                "testing/version-link.c",
                "testing/version.c",
            ]
