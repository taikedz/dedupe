import unittest

import ddresolutions as ddrns

import resolvers.FileDelete
import resolvers.DirDelete
import resolvers.DirMerge

class MainResolutionsTest(unittest.TestCase):
    def test_resolution_dispatch(self):
        print("\nResolution dispatch tests")

        class MockIdentity:
            def __str__(self):
                return "MockIdentity"

            def showPaths(self):
                print(".... (displaying paths to resolve) ...")
        
        ddres = ddrns.DDResolutions()

        handler = ddres.getUserResolver(MockIdentity(), default_selection=0 )
        print("Selected <<%s>>" % str(handler))
        self.assertIsInstance(handler, resolvers.FileDelete.FileDeleteResolver)

        handler = ddres.getUserResolver(MockIdentity(), default_selection=1 )
        print("Selected <<%s>>" % str(handler))
        self.assertIsInstance(handler, resolvers.DirDelete.DirDeleteResolver)

        handler = ddres.getUserResolver(MockIdentity(), default_selection=2 )
        print("Selected <<%s>>" % str(handler))
        self.assertIsInstance(handler, resolvers.DirMerge.DirMergeResolver)

if __name__ == "__main__":
    unittest.main()
