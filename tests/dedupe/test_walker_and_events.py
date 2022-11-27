import os
from unittest import TestCase

from dedupe.walker import DedupeWalker
from dedupe import event

from tests import tempfs 

def register_git_dir_path(path):
    if os.path.isdir(os.path.join(path, '.git')):
        raise event.DedupeSkip(path)

class TestDedupeWalker(TestCase):
    test_filesystem = """
    vegetable:
        fruit:
            apple: red
            banana: yellow

        salad:
            tomato: red
            lettuce: green

        # Should not appear in the results
        repo:
            .git:
            raw_food: unprocessed
            bin:
                compost: rotten
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.tempfs = tempfs.TempFilesystem(cls.test_filesystem)
        cls.walker = DedupeWalker("vegetable")
        event.register_handler("DIR-HASH", register_git_dir_path)


    @classmethod
    def tearDownClass(cls):
        cls.tempfs.cleanup()


    def setUp(self):
        self.names = []
        print(f"---------------\n{self.id()}")


    def test_file_handlers(self):

        event.register_handler("FILE-HASH",
            lambda name: self.names.append(name))

        self.walker.walk_folder()

        self.names.sort()

        expected = [
            "vegetable/fruit/apple",
            "vegetable/fruit/banana",
            "vegetable/salad/lettuce",
            "vegetable/salad/tomato"
            ]
        expected.sort()
        assert self.names == expected, f"Got {self.names}"


    def test_dir_handlers(self):

        event.register_handler("DIR-HASH",
            lambda name: self.names.append(name))

        self.walker.walk_folder()

        self.names.sort()

        expected = ["vegetable/fruit", "vegetable/salad", "vegetable"]
        expected.sort()
        assert self.names == expected, f"Got {self.names}"
