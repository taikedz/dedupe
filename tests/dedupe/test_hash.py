import unittest
import os

from dedupe.hash import hash_bytes, hash_file

class TestHash(unittest.TestCase):
        def test_hash(self):
            assert hash_bytes(b"stuff") == "5eee38381388b6f30efdd5c5c6f067dbf32c0bb3", (
                "Incorrect hash")

            test_text = b"this is some text"
            test_file = "local_test"
            with open(test_file, 'wb') as fh:
                fh.write(test_text)
            
            assert hash_bytes(test_text) == hash_file(test_file, 4), "Mismatched hash"
            assert hash_bytes(test_text[:8]) == hash_file(test_file, 4, 8), "Mismatched hash"
            assert hash_bytes(test_text[:10]) == hash_file(test_file, 4, 10), "Mismatched hash"

            os.remove(test_file)
