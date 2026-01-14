import fnmatch
from pathlib import Path
from dedupe import config

_IGNORE_SPEC:dict[str,list[str]] = {
    "name": [],
    "beacon" : [],
}

def load_ignores(path:str=''):
    if path == '':
        path = config.IGNORE_FILE

    with open(path) as fh:
        for line in fh.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("./"):
                _IGNORE_SPEC["beacon"].append(line)
            else:
                _IGNORE_SPEC["name"].append(line)


def should_ignore(itempath):
    itempath = Path(itempath)
    if itempath.is_dir() and should_ignore_dir(itempath):
        return True
    return should_ignore_name(itempath.name)


def should_ignore_dir(itempath):
    res = [(Path(itempath)/p).exists() for p in _IGNORE_SPEC["beacon"]]
    print(f"DIR -> {itempath} : {res}")
    return any(res)


def should_ignore_name(itemname):
    res = [fnmatch.filter([itemname], pat) for pat in _IGNORE_SPEC["name"]]
    print(f"NAME -> {itemname} : {res}")
    return any(res)
