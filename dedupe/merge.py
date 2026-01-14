import os
from pathlib import Path

from dedupe import fs, ignore
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

    dfiles = fs.all_files(dest)
    dabspaths = [Path(f).absolute() for f in dfiles if Path(f).is_file()]

    sfiles = [source/p for p in os.listdir(source)]
    sabspaths = [f.absolute() for f in sfiles if f.is_file()]

    # Ensure all duplicate hashes have been calculated upfront
    [db.addFile(path) for path in dabspaths+sabspaths if not ignore.should_ignore(path)]

    dhashes = [db.hashForPath(d) for d in dabspaths]
    assert None not in dhashes, f"Fatal: Error in file registration!"

    fullhashes = [f for p,_s,f in dhashes]

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

    with HashRegistry() as db:
        for parent, folders, _f in os.walk(source):
            rel_parent = PathOp(parent) - source

            if (dest/rel_parent).is_file():
                raise RuntimeError(f"{dest/rel_parent} already exists and is not a directory")
            os.makedirs(dest/rel_parent, exist_ok=True)

            _merge_files(dest/rel_parent, source/rel_parent, db)

            # Iterate the folders - if any should be ignored, remove them in-place
            #  from the folders list, to avoid descending into them
            inspect_dirs = folders[:]
            for d in inspect_dirs:
                if ignore.should_ignore(f"{parent}/{d}"):
                    folders.remove(d)




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