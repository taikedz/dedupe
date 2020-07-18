import unittest

import testutils as TU

import DirWalker
import Handlers
import ddlog
import ddexceptions as DDE

identify_list = []
file_list = []
dir_list = []
enter_list = []

class Appender:
    def __init__(self, listref, mode):
        self.target_list = listref
        self.mode = mode

    def __call__(self, item):
        if self.mode == "encounter":
            if "exclude" in item.getName():
                raise DDE.ProcessorSkipException(f"Skipping {item} (name)")
            else:
                self.target_list.append(str(item) )

        elif self.mode == "enter":
            if "thing.project" in item.getContents():
                raise DDE.ProcessorSkipException(f"Skipping {item} (project)")
            else:
                self.target_list.append(str(item) )

        elif self.mode == "identify":
            if "anon" in item.getName():
                raise DDE.ProcessorSkipException(f"Skipping {item} (name)")
            else:
                self.target_list.append(str(item) )

class TestDirWalker(unittest.TestCase):
    """ A blind test item to ensure DirWalker runs without
    glaring errors

    We are testing its walk, not the underlying handlers
    """

    def checkPath(self, path, target_list):
        self.assertTrue(path in target_list)

    def forbidPath(self, path, target_list):
        self.assertTrue(path not in target_list)

    def runTest(self):
        dw = DirWalker.DirWalker(TU.getPath())
        dw.walk()

        #print(f"Dirs: {dir_list}")
        #print(f"Entered: {enter_list}")
        #print(f"Files: {file_list}")

        self.assertTrue(TU.getPath("firstdir/subdir") in dir_list)
        self.assertTrue(TU.getPath("seconddir") in dir_list)
        self.assertTrue(TU.getPath("firstdir/exclude") not in dir_list) # Encountered and immediately excluded
        self.assertTrue(TU.getPath("projectdir") in dir_list) # Encountered, and not excluded by name...
        self.assertTrue(TU.getPath("projectdir/src") not in dir_list) # ... but not entered ...

        self.assertTrue(TU.getPath("firstdir/subdir") in enter_list)
        self.assertTrue(TU.getPath("seconddir") in enter_list)
        self.assertTrue(TU.getPath("firstdir/exclude") not in enter_list)
        self.assertTrue(TU.getPath("projectdir") not in enter_list) # .... so not registered for entry
        self.assertTrue(TU.getPath("projectdir/src") not in enter_list)

        self.assertTrue(TU.getPath("firstdir/subdir/file1") in file_list)
        self.assertTrue(TU.getPath("seconddir/file2") in file_list)
        self.assertTrue(TU.getPath("firstdir/exclude/somefile") not in file_list)
        self.assertTrue(TU.getPath("seconddir/exclude_file") not in file_list)
        self.assertTrue(TU.getPath("projectdir/thing.project") not in file_list)
        self.assertTrue(TU.getPath("projectdir/src/thing.sh") not in file_list)

        self.assertTrue(TU.getPath("firstdir/subdir/file1") in identify_list)
        self.assertTrue(TU.getPath("seconddir/file2") in identify_list)
        self.assertTrue(TU.getPath("firstdir/exclude/somefile") not in identify_list)
        self.assertTrue(TU.getPath("seconddir/exclude_file") not in identify_list)
        self.assertTrue(TU.getPath("projectdir/thing.project") not in identify_list)
        self.assertTrue(TU.getPath("projectdir/src/thing.sh") not in identify_list)
        self.assertTrue(TU.getPath("anonymous") not in identify_list)

    def setUp(self):
        TU.touch("firstdir/subdir/file1", "hello")
        TU.touch("firstdir/exclude/somefile", "irrelevant")
        TU.touch("seconddir/file2", "goodbye")
        TU.touch("seconddir/exclude_file", "absurd")
        TU.touch("projectdir/thing.project", "project meta data")
        TU.touch("projectdir/src/thing.sh", "echo hello")
        TU.touch("anonymous", "do not id me")

        Handlers.registerWalkEventHandler(Handlers.EVT_ENTER_DIR, "register enter dir", Appender(enter_list, "enter") )
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_DIR, "register encounter dir", Appender(dir_list, "encounter") )
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_FILE, "register encounter file",  Appender(file_list, "encounter") )
        Handlers.registerWalkEventHandler(Handlers.EVT_IDENTIFY, "register identify file",  Appender(identify_list, "identify") )

    def tearDown(self):
        TU.removeTmp()

if __name__ == '__main__':
    unittest.main()
