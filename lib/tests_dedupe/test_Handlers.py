import unittest

import testutils as TU

import Handlers

class TestHandlerRegistration(unittest.TestCase):

    def runTest(self):

        def processing_stub(target_item):
            TU.store( "stub", str(target_item) )

        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_FILE, "processing_stub", processing_stub)
        Handlers.registerWalkEventHandler(Handlers.EVT_ENCOUNTER_DIR, "processing_stub", processing_stub)

        all_handlers = Handlers.getHandlers()

        enc_file_handler = all_handlers[Handlers.EVT_ENCOUNTER_FILE][0]
        enc_file_handler.process("the_file")

        self.assertEqual(TU.retrieve("stub"), "the_file")

        enc_dir_handler = all_handlers[Handlers.EVT_ENCOUNTER_DIR][0]
        enc_dir_handler.process("the_dir")

        self.assertEqual(TU.retrieve("stub"), "the_dir")

        self.assertEqual(len(all_handlers[Handlers.EVT_ENTER_DIR]) , 0 )
        self.assertEqual(len(all_handlers[Handlers.EVT_ENCOUNTER_DIR]) , 1 )
        self.assertEqual(len(all_handlers[Handlers.EVT_ENCOUNTER_FILE]) , 1 )

if __name__ == '__main__':
    unittest.main()
