import hashlib
import os

_hashfunc=hashlib.sha1

def hash_bytes(data):
    return _hashfunc(data).hexdigest()


def hash_file(path:str, chunk_size:int=1024*1024, max_bytes:int=0):
    """ Basic file hashing function.

    :param path: Path to the file to derive a hash for

    :param chunk_size: How many bytes of the file to read at a time.

    :param max_bytes: How many bytes of the file to read before stopping (partial file hash)
    """
    h_obj = _hashfunc()
    byte_count = 0

    with open(path, 'rb') as fh:
        data = None
        while data != b'':
            to_read = min(max_bytes-byte_count, chunk_size) if max_bytes > 0 else chunk_size
            data = fh.read(to_read)
            byte_count += to_read

            h_obj.update(data)

            if max_bytes > 0 and byte_count >= max_bytes: break

    return h_obj.hexdigest()



if __name__ == "__main__":
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

    print("Basic tests passed")
