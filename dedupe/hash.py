import hashlib

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

