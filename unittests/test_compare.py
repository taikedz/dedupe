from argparse import Namespace
from dedupe import compare
from unittests.makefiles import FileSet


class TestCompare:
    def testCompareNoDupes(self):
        fileset = {
            "artists/1-leo": "leonardo",
            "artists/2-pic": "picasso",
            "artists/3-raph": "raphael",
            "artists/4-miro": "miro",

            # "artists/modern/picasso": "picasso",
            # "artists/modern/dali": "dali",

            "turtles/1-leo": "leonardo",
            "turtles/2-don": "donatello",
            "turtles/3-raph": "raphael",
            "turtles/4-mick": "michaelangelo",
        }

        args = Namespace()
        args.path1 = "testing/artists"
        args.path2 = "testing/turtles"
        with FileSet("testing", fileset):
            assert compare._compare(args) == {
                '/home/tai/git/github.com/taikedz/dedupe/testing/artists/1-leo': ['/home/tai/git/github.com/taikedz/dedupe/testing/turtles/1-leo'],
                '/home/tai/git/github.com/taikedz/dedupe/testing/artists/3-raph': ['/home/tai/git/github.com/taikedz/dedupe/testing/turtles/3-raph'],
            }