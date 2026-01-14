import os
from pathlib import Path
from dedupe import ignore, registry
from unittests.makefiles import FileSet


class TestIgnore:
    def testIgnore(self):
        files = {
            "readme.txt":"hi",
            "info.md":"instruction",
            "repo/.git/config":"data",
            "repo/license.txt":"license",
            ".venv/bin/activate":"python",
            ".venv/pip.txt":"fruit",
            "._DSStore":"apples",
            "._info.md":"pears",
            "._readme.txt":"stairs",
        }

        ignorefile = "myignore.txt"
        try:
            with open(ignorefile, "w") as fh:
                for pat in ["._*", "*.venv", "", "# other things to ignore", "./.git"]:
                    fh.write(f"{pat}\n")
            ignore.load_ignores(ignorefile)

            assert ignore._IGNORE_SPEC["name"] == ["._*", "*.venv"]
            assert ignore._IGNORE_SPEC["beacon"] == ["./.git"]

            with FileSet("testing", files):
                with registry.HashRegistry() as db:
                    db.registerDir("testing")
                    registered_files = [x[0] for x in db._cursor.execute("SELECT path FROM HashedFiles") ]
                    assert registered_files == [str(Path(f).absolute()) for f in ["testing/readme.txt", "testing/info.md"]]
        finally:
            os.remove(ignorefile)