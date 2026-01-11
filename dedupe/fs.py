import os
import pathlib
from typing import Generator


class PathOp(pathlib.Path):

    def absolute(self):
        return PathOp(pathlib.Path.absolute(self))
    

    def parts(self):
        return tuple(s for s in str(self.absolute()).split("/") if s)
    

    def __sub__(self, other):
        other_parts = list(PathOp(other).absolute().parts())
        my_parts = list(self.absolute().parts())

        while other_parts and my_parts and other_parts[0] == my_parts[0]:
            other_parts.pop(0)
            my_parts.pop(0)

        if other_parts:
            return None
        
        return PathOp(os.path.sep.join(my_parts))


    def hasChildOrIsSame(self, other) -> bool:
        other = PathOp(other)

        other_parts = other.parts()
        self_parts = self.parts()

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


if __name__ == "__main__":
    p = PathOp("this/that")
    assert p.hasChildOrIsSame("this/that")
    assert p.hasChildOrIsSame("this/that/then")

    assert not p.hasChildOrIsSame("this")
    assert not p.hasChildOrIsSame("this/then")
    assert not p.hasChildOrIsSame("that")
    assert not p.hasChildOrIsSame("then")

    diff = PathOp("one/two/three/four") - "one/two"
    assert diff == PathOp("three/four"), diff

    diff = PathOp("one/two") - "one/two/three"
    assert diff == None, diff

    diff = PathOp("one/two/three") - "one/two/four"
    assert diff == None, diff