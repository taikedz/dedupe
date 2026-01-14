import os

from dedupe import ignore
from dedupe.registry import HashRegistry


def run(args):
    res = _compare(args)
    for path,dupes in res.items():
        print(f"Duplicates for '{path}': {[f'  {p}' for p in dupes]}")


def _compare(args):
    # straight compare - just the files under here
    files1 = os.listdir(args.path1)
    files2 = os.listdir(args.path2)

    results = {}

    with HashRegistry() as db:
        add_hashes = lambda p_list: [db.hashForPath(p, add=True) for p in p_list if not ignore.should_ignore(p)]
        hashpaths1 = add_hashes( [f"{args.path1}/{f1}" for f1 in files1] )
        hashpaths2 = add_hashes( [f"{args.path2}/{f2}" for f2 in files2] )

    shorts2 = [row[1] for row in hashpaths2]
    hashes2 = [row[2] for row in hashpaths2]

    for path, shorthash, hash in hashpaths1:
        dupes = []
        if hash and hash in hashes2:
            dupes = [p for p,_,hash2 in hashpaths2 if hash == hash2]
        elif shorthash in shorts2:
            dupes = [p for p,short2,_ in hashpaths2 if shorthash == short2]
        if dupes:
            results[path] = dupes

    return results
