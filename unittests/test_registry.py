import re

from dedupe import registry
from unittests.util import FileSet, RegistryTest


class TestFind(RegistryTest):
    def test_find(self):
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
            with registry.HashRegistry() as db:
                db.registerDir("testing")
                entries = db.allDupeEntries()
                short_entries = [(m.group(1), hash) for path,hash in entries if (m := re.match(".+?/testing/(.+)", path))]
                assert sorted(short_entries, key=lambda t: t[0]) == [
                        ("old-src/readme.txt", "c22b5f9178342609428d6f51b2c5af4c0bde6a42"),
                        ("readme.txt", "c22b5f9178342609428d6f51b2c5af4c0bde6a42"),
                        ]
