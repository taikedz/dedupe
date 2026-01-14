import os
from pathlib import Path
from dedupe import merge
from dedupe.registry import HashRegistry


def flatten(dirpath:str):
    with HashRegistry() as db:
        db.registerDir(dirpath)

    rootpath = Path(dirpath)
    for subdir in [rootpath/d for d in os.listdir(dirpath) if (rootpath/d).is_dir()]:
        for targetDir, _d, _f in os.walk(subdir):
            merge.merge(dirpath, targetDir)
