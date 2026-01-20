import os
import pathlib
from typing import Generator


class FileError(Exception):
    pass


def all_files(path, regular_only=False):
    items = []
    for parent,_folders,files in os.walk(path):
        items.extend([f"{parent}/{f}" for f in files])
    if regular_only:
        items = [f for f in items if is_regular(f)]
    return sorted(items)


class PathOp(pathlib.Path):

    def absolute(self):
        return PathOp(pathlib.Path.absolute(self).resolve())
    

    def path_parts(self):
        return [s for s in str(self.absolute()).split("/") if s]
    

    def __sub__(self, other):
        other_parts = list(PathOp(other).absolute().path_parts())
        my_parts = list(self.absolute().path_parts())

        while other_parts and my_parts and other_parts[0] == my_parts[0]:
            other_parts.pop(0)
            my_parts.pop(0)

        if other_parts:
            return None
        
        return PathOp(os.path.sep.join(my_parts))


    def hasChildOrIsSame(self, other) -> bool:
        other = PathOp(other)

        other_parts = other.path_parts()
        self_parts = self.path_parts()

        if self_parts == other_parts:
            return True
        
        for self_part, child_part in _zip_more(self_parts, other_parts):
            if self_part is None:
                return True
            if self_part != child_part:
                return False

        raise RuntimeError(
            f"Impossible point reached when processing:\n"
            f" ---\n"
            f"    {repr(self_parts)}\n"
            f" ---\n"
            f"    {repr(other_parts)}\n"
            f" ===\n"
            )


def _zip_more(iter1:list[str], iter2:list[str]) -> Generator[tuple[str,str], None, None]:
    n1, n2 = 0,0

    while True:
        item1 = None
        if n1 < len(iter1):
            item1 = iter1[n1]

        item2 = None
        if n2 < len(iter2):
            item2 = iter2[n2]

        if (item1, item2) == (None, None):
            break

        yield (item1, item2)

        n1 += 1
        n2 += 1


def is_regular(path):
    """ Whether path is a regular file or folder, and is _not_ a symlink
    """
    if os.path.islink(path):
        return False
    if not os.path.exists(path):
        raise FileError(f"Expected '{path}' to exist, but it does not.")
    return (os.path.isfile(path) or os.path.isdir(path))

