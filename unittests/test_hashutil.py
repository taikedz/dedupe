import os
from dedupe import hashutil


class TestHashUtil:
    def testHashFile(self):
        tempfile = "data.temp"
        with open(tempfile, 'w') as fh:
            fh.write("deduplication facilitation")

        try:
            assert hashutil.hash_file(tempfile, max_bytes=13) == "b7b4e44e38fc1dcbaeb7cab4bb610c03e6e5ff7c"
            assert hashutil.hash_file(tempfile) == "fc01ec23d2e30ca141a17400bcbd9d447b9e1ae1"
        finally:
            os.remove(tempfile)


    def testHashString(self):
        assert hashutil.hash_string("deduplicate") == "6369779dd2424d4555fc64df7af8649cc9c4d2b4"