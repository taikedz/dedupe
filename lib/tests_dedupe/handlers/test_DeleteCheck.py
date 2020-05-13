import unittest

import testutils as TU

import ddexceptions as DDE

#import ddlog
#log = ddlog.getLogger(level="DEBUG")

# ======================
import ddpreferences as DDPREF
TU.touch("config.yaml", data="""
config:
  encounters:
    DeleteCheck:
      file: [".DS_Store"]
""")
DDPREF.loadPreferences(TU.getPath("config.yaml"))
# --------

import handlers.DeleteCheck as DC

files_to_process = [
        "config.yaml",
        "myfile",
        "stuff.DS_Store",
        ".DS_Store",
        ".DS_store.bak",
        "x.DS_store.bak",
]
files_to_process.sort()

class TestDeleteCheck(unittest.TestCase):
    def setUp(self):
        for item in files_to_process:
            TU.touch(item)

    def tearDown(self):
        TU.removeTmp()

    def runTest(self):
        for item in files_to_process:
            if item == ".DS_Store":
                with self.assertRaises(DDE.ProcessorSkipException) as cm:
                    DC.process(TU.getWalkerItemFrom(item) )
            else:
                DC.process(TU.getWalkerItemFrom(item) )

        remaining = TU.getWalkerItemFrom("").getContents()
        remaining.sort()
        expected_remaining = files_to_process.copy()
        expected_remaining.remove(".DS_Store")
        expected_remaining.sort()

        self.assertNotEqual(expected_remaining, files_to_process)
        self.assertEqual(expected_remaining, remaining)
        
if __name__ == "__main__":
    unittest.main()
