from dedupe import merge
from unittests.makefiles import FileSet
from unittests.util import RegistryTest


class TestMerge(RegistryTest):

    def testMerge(self):
        fileset = {
            "artists/genius/a1-leo": "leonardo",
            "artists/a2-pic": "picasso",
            "artists/a3-raph": "raphael",
            "artists/a4-miro": "miro",

            "artists/modern/picasso": "picasso",
            "artists/modern/dali": "dali",

            "turtles/leader/t1-leo": "leonardo",
            "turtles/t2-don": "donatello",
            "turtles/t3-raph": "raphael",
            "turtles/t4-mick": "michaelangelo",
        }

        artists = "testing/artists"
        turtles = "testing/turtles"
        with FileSet("testing", fileset) as fs:
            merge.merge_deep(artists, turtles)

            assert fs.all_files() ==  [
                'testing/artists/a2-pic',
                'testing/artists/a3-raph',
                'testing/artists/a4-miro',
                'testing/artists/genius/a1-leo',
                'testing/artists/modern/dali',
                'testing/artists/modern/picasso',
                'testing/artists/t2-don',
                'testing/artists/t4-mick',
                # t1-leo stays in turtles, because deep file genius/a1-leo takes precedence in destination
                'testing/turtles/leader/t1-leo',
                'testing/turtles/t3-raph',
            ]