import unittest

import testutils as TU

#import ddlog
#log = ddlog.getLogger("DEBUG")

import ddexceptions as DDE

# ======================
import ddpreferences as DDPREF
TU.touch("config.yaml", data="""
config:
  encounters:
    DirectoryContentCheck:
      file: ["*.aup", "*.kdenlive"]
      dir: [".git", ".svn"]
""")
DDPREF.loadPreferences(TU.getPath("config.yaml"))
# --------

import handlers.DirectoryContentCheck as DCC

class TestDirContentCheck(unittest.TestCase):
    def setUp(self):
        TU.touch("folder1/.git") # Is a file, so should not trigger repo
        TU.touch("folder2/.git/repodata")
        TU.touch("folder3/recording.aup")
        TU.touch("folder4/various")

    def tearDown(self):
        TU.removeTmp()

    def runTest(self):
        # We test only the top level fodlers,
        # as this event is fired during EVT_ENTER_DIR
        DCC.process(TU.getWalkerItemFrom("folder1/"))
        DCC.process(TU.getWalkerItemFrom("folder4/"))
        self.bounces(TU.getWalkerItemFrom("folder2/"))
        self.bounces(TU.getWalkerItemFrom("folder3/"))

    def bounces(self, path):
        with self.assertRaises(DDE.ProcessorSkipException) as cm:
            DCC.process(path)

if __name__ == "__main__":
    unittest.main()
