import unittest
import ddlog

import testutils as TU

import DirWalker
import Handlers

file_list = []
dir_list = []
enter_list = []

class Appender:
    def __init__(self, listref):
        self.target_list = listref

    def __call__(self, item):
        self.target_list.append(str(item) )

class TestDirWalker(unittest.TestCase):
    """ A blind test item to ensure DirWalker runs without
    glaring errors
    """

    def runTest(self):
        dw = DirWalker.DirWalker(TU.getPath())
        dw.walk()

        self.assertTrue( TU.getPath("firstdir/subdir/file1") in file_list )
        self.assertTrue( TU.getPath("firstdir/subdir/file2") in file_list )
        self.assertTrue( TU.getPath("firstdir/subdir/file3") in file_list )
        self.assertTrue( TU.getPath("seconddir/file4") in file_list )
        self.assertTrue( TU.getPath("seconddir/file4") in file_list )

    def setUp(self):
        TU.touch("firstdir/subdir/file1", "hello")
        TU.touch("firstdir/subdir/file2", "greetings")
        TU.touch("firstdir/subdir/file3", "bye")
        TU.touch("seconddir/file4", "hello")
        TU.touch("seconddir/file5", "goodbye")

        Handlers.registerWalkEventHandler(Handlers.EVT_ENTER_DIR, "register enter dir", Appender(enter_list) )
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_FILE, "register encounter file",  Appender(file_list) )
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_DIR, "register encounter dir", Appender(dir_list) )

    def tearDown(self):
        TU.removeTmp()

def runplain():
    TU.touch("firstdir/subdir/file1", "hello")
    TU.touch("firstdir/subdir/file2", "greetings")
    TU.touch("firstdir/subdir/file3", "bye")
    TU.touch("seconddir/file4", "hello")
    TU.touch("seconddir/file5", "goodbye")
    dw = DirWalker.DirWalker(TU.getPath())
    dw.walk()
    TU.removeTmp()

if __name__ == '__main__':
    unittest.main()
