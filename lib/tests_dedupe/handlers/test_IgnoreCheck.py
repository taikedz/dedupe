import unittest

import testutils as TU

import ddexceptions as DDE

import ddlog
log = ddlog.getLogger()

# ======================
import ddpreferences as DDPREF
TU.touch("config.yaml", data="""
config:
  encounters:
    IgnoreCheck:
      file: ["*.pyc"]
      dir: ["__pycache__"]
""")
DDPREF.loadPreferences(TU.getPath("config.yaml"))
# --------

import handlers.IgnoreCheck as IC

files_to_process = [
    "config.yaml",
    "file1",
    "__pycache__/dummy",
    "igfile1.py",
    "igfile2.pyc",
    "igfile3.pyc.bar",
]
files_to_process.sort()

class TestDeleteCheck(unittest.TestCase):
    def setUp(self):
        for item in files_to_process:
            TU.touch(item)

    def tearDown(self):
        TU.removeTmp()

    def runTest(self):
        # Note - we are not testing a walk here
        # only that the right files trigger the ProcessorSkipException
        for item in files_to_process:
            log.debug("> "+item)
            if item == "__pycache__" or item[-4:] == ".pyc":
                # Exception here is OK ...
                with self.assertRaises(DDE.ProcessorSkipException) as cm:
                    IC.process(TU.getWalkerItemFrom(item) )
            else:
                # ... but here it is not
                IC.process(TU.getWalkerItemFrom(item) )
        
if __name__ == "__main__":
    unittest.main()
