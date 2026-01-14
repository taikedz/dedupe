from dedupe import merge
from unittests.makefiles import FileSet
from unittests.util import RegistryTest


class TestMerge(RegistryTest):

    def testCompareNoDupes(self):
        fileset = {
            "artists/leader/a1-leo": "leonardo",
            "artists/a2-pic": "picasso",
            "artists/a3-raph": "raphael",
            "artists/a4-miro": "miro",

            "artists/modern/picasso": "picasso",
            "artists/modern/dali": "dali",

            "turtles/t1-leo": "leonardo",
            "turtles/t2-don": "donatello",
            "turtles/t3-raph": "raphael",
            "turtles/t4-mick": "michaelangelo",
        }

        artists = "testing/artists"
        turtles = "testing/turtles"
        with FileSet("testing", fileset) as fs:
            merge.merge(artists, turtles)
            assert fs.all_files() ==  [
                'testing/artists/leader/a1-leo',
                'testing/artists/t2-don',
                'testing/artists/a2-pic',
                'testing/artists/a3-raph',
                'testing/artists/t4-mick',
                'testing/artists/a4-miro',
                'testing/artists/modern/dali',
                'testing/artists/modern/picasso',
                'testing/turtles/t1-leo',
                'testing/turtles/t3-raph',
            ]