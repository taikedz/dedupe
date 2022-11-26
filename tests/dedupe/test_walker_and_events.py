from unittest import TestCase

from dedupe.walker import DedupeWalker
from dedupe import event

from tests import tempfs 


class TestDedupeWalker(TestCase):
    test_filesystem = """
    vegetable:
        fruit:
            apple: red
            banana: yellow

        salad:
            tomato: red
            lettuce: green
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.tempfs = tempfs.TempFilesystem(cls.test_filesystem)
        cls.walker = DedupeWalker()


    @classmethod
    def tearDownClass(cls):
        cls.tempfs.cleanup()


    def setUp(self):
        self.names = []
        print(f"---------------\n{self.id()}")


    def test_file_handlers(self):

        event.register_handler("FILE-HASH",
            lambda name: self.names.append(name))

        self.walker.walk_folder("vegetable")

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

        self.walker.walk_folder("vegetable")

        self.names.sort()

        expected = ["vegetable/fruit", "vegetable/salad", "vegetable"]
        expected.sort()
        assert self.names == expected, f"Got {self.names}"
