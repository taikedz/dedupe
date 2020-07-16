import unittest

import testutils as TU

import Handlers
from WalkerItem import WalkerItem

class TestHandlerRegistration(unittest.TestCase):

    def runTest(self):

        def processing_stub(target_item):
            TU.store( "stub", str(target_item) )

        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_FILE, "processing_stub", processing_stub)
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_DIR, "processing_stub", processing_stub)

        Handlers.processEvent(Handlers.EVT_ENCOUNTER_FILE, TU.getWalkerItemFrom("the_file") )
        self.assertEqual(TU.retrieve("stub"), TU.getPath("the_file"))

        Handlers.processEvent(Handlers.EVT_ENCOUNTER_DIR, TU.getWalkerItemFrom("the_dir") )
        self.assertEqual(TU.retrieve("stub"), TU.getPath("the_dir"))

    def setUp(self):
        TU.touch("the_file", "data")
        TU.touch("the_dir/dummy", "data")

    def tearDown(self):
        TU.removeTmp()

if __name__ == '__main__':
    unittest.main()
