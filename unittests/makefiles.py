import os
from pathlib import Path
import shutil


class FileSet:
    def __init__(self, holddir:str, files:dict[str,str]):
        self._hdir = Path(holddir)
        self._fileset = files


    def __enter__(self):
        self.make_files()
        return self
    

    def __exit__(self, *e):
        self.delete_files()


    def make_files(self):
        for path,data in self._fileset.items():
            path = self._hdir/path
            parent = path.parent
            os.makedirs(parent, exist_ok=True)
            with open(path, 'w') as fh:
                fh.write(data)


    def delete_files(self):
        shutil.rmtree(self._hdir)


    def all_files(self) -> list[str]:
        items = []
        for parent,_folders,files in os.walk(self._hdir):
            items.extend([f"{parent}/{f}" for f in files])
        return sorted(items)
