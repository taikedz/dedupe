import os
from pathlib import Path

from dedupe import hashutil
from dedupe.fs import PathOp
from dedupe.registry import HashRegistry


def do_merge(dest_path, source_path, recursive):
    if recursive:
        merge_deep(dest_path, source_path)
    else:
        merge(dest_path, source_path)


def merge(dest_path, source_path):
    with HashRegistry() as db:
        _merge_files(dest_path, source_path, db)


def _merge_files(dest_path, source_path, db:HashRegistry):
    dest = Path(dest_path).absolute()
    source = Path(source_path).absolute()

    dfiles = [dest/p for p in os.listdir(dest)]
    dabspaths = [f.absolute() for f in dfiles if f.is_file()]

    sfiles = [source/p for p in os.listdir(source)]
    sabspaths = [f.absolute() for f in sfiles if f.is_file()]

    # Ensure all duplicate hashes have been calculated upfront
    [db.addFile(path) for path in dabspaths+sabspaths]

    dhashes = [db.hashForPath(d, add=True) for d in dabspaths]
    fullhashes = [f for _p,_s,f in dhashes]

    for spath in sabspaths:
        _p,_s, s_full = db.hashForPath(spath, add=True)
        if s_full and s_full in fullhashes:
            pass # os.remove(spath)
        # let the user do removal afterwards
        else:
            destfile = dest/spath.name
            if destfile.exists():
                destfile = _getUniqueName(destfile)
            os.rename(spath, destfile)


def merge_deep(dest_dir, source_dir):
    dest = Path(dest_dir)
    source = Path(source_dir)

    name = hashutil.hash_string(str(dest.absolute()))
    regtemp = f"/tmp/{name}.sqlite"

    with HashRegistry(regtemp, temp=True) as db:
        for parent, folders, _ in os.walk(source):
            rel_parent = PathOp(parent) - source

            if (dest/rel_parent).is_file():
                raise RuntimeError(f"{dest/rel_parent} already exists and is not a directory")
            os.makedirs(dest/rel_parent, exist_ok=True)

            _merge_files(dest/rel_parent, source/rel_parent, db)




def _getUniqueName(file:Path):
    maxiter = 256
    x = 1
    parent = file.parent
    name = file.name
    while True:
        newname = (parent/f"{name}-{x}")
        if not newname.exists():
            return newname
        x +=1
        assert x <= maxiter, f"Could not generate new name for {file} beyond {maxiter} tries"