import unittest

import ddpreferences as DDPREF
import ddexceptions as DDE
import ddlog

import testutils

#ddlog.setLevel("DEBUG")

DDPREF.loadPreferences(None)
import handlers.SymLinkCheck as checker

class TestSymLinkAvoidance(unittest.TestCase):
    def setUp(self):
        testutils.touch("folder1/file1")
        testutils.touch("folder2/file2", symlink_source="folder1/file1")
        testutils.touch("folder2/file3", symlink_source="nonexistent")

    def runTest(self):
        wi = testutils.getWalkerItemFrom("folder1/file1")
        # FIXME -- wait WHAT are we testing??
        with self.assertRaises(AssertionError) as cm1: # No native assertNotRaises in unittest...
            with self.assertRaises(DDE.ProcessorSkipException) as cm2:
                checker.process(wi)

        wi = testutils.getWalkerItemFrom("folder2/file2")
        with self.assertRaises(DDE.ProcessorSkipException) as cm:
            checker.process(wi)

        wi = testutils.getWalkerItemFrom("folder2/file3")
        with self.assertRaises(DDE.ProcessorSkipException) as cm:
            checker.process(wi)

    def tearDown(self):
        testutils.removeTmp()

if __name__ == "__main__":
    unittest.main()
