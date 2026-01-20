import os

from unittests.util import FileSet

class TestFileSet:
    def test_fileset_links(self):
        with FileSet("linkos", {"src-link ->" :"dest-link"}) as fset:
            allfiles = fset.all_files()
            assert allfiles == ["linkos/src-link"]
            assert os.path.islink("linkos/src-link")

