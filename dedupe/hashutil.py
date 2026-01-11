import hashlib

SHORT_BYTES = 4096


def shortHash(path:str) -> str:
    return hash_file(path, max_bytes=SHORT_BYTES)


def fullHash(path:str) -> str:
    return hash_file(path)


def hash_file(path:str, chunk_size:int=1024*1024, max_bytes:int=0, hash_func=hashlib.sha1) -> str:
    """ Basic file hashing function.

    :param path: Path to the file to derive a hash for

    :param chunk_size: How many bytes of the file to read at a time.

    :param max_bytes: How many bytes of the file to read before stopping (partial file hash)

    :param hash_func: Function returning an updatable hashing object
    """
    h_obj = hash_func()
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


def hash_string(data:str) -> str:
    hasher = hashlib.sha1()
    hasher.update(bytes(data, 'utf-8'))
    return hasher.hexdigest()