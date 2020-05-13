import unittest

import testutils as TU
import WalkerItem as W

class TestWalkerItem(unittest.TestCase):
    def setUp(self):
        TU.touch("topfolder/singlefile")
        TU.touch("topfolder/subfolder/alink", symlink_source="topfolder/singlefile")
        TU.touch("topfolder/subfolder/blink", symlink_source="nonexistent")

    def tearDown(self):
        TU.removeTmp()

    def runTest(self):
        root_dir = TU.getPath("")
        top_dir = TU.getPath("topfolder")

        top_walker = W.WalkerItem(top_dir, "topfolder")

        self.assertEqual(top_dir, str(top_walker))
        self.assertEqual(top_dir, top_walker.getFullPath())
        self.assertEqual(top_walker.getContents(), ["singlefile", "subfolder"])
        self.assertTrue(top_walker.isdir())

        alink_walker = W.WalkerItem(TU.getPath("topfolder/subfolder/alink"), top_dir)
        self.assertEqual(TU.getPath("topfolder/subfolder/alink"), str(alink_walker))
        self.assertTrue(alink_walker.isfile())
        self.assertTrue(alink_walker.islink())

        blink_walker = W.WalkerItem(TU.getPath("topfolder/subfolder/blink"), top_dir)
        self.assertEqual(TU.getPath("topfolder/subfolder/blink"), str(blink_walker))
        self.assertTrue(blink_walker.islink())
        self.assertFalse(blink_walker.isfile())

if __name__ == "__main__":
    unittest.main()
