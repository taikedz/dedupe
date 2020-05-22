import os

_subtitutes = {
    "%CWD%" : os.getcwd(),
    "%HOME%" : os.path.expanduser("~"),
}

global_config_paths = [
    "%CWD%/Dedupe.yaml",
    "%HOME%/.local/lib/dedupe/Dedupe.yaml",
]

def _doSubstitutions(path):
    for sub in _substitutes.keys():
        path.replace(sub, _substitutes[sub])

def resolve(path):
    """ Resolve a path.

    Paths are typically expressed as UNIX-style paths (with '/' separator), and can have placeholders.

    This function replaces elements as appropriate, as well as converting to the local mode of expression of paths
    (different between Windows and UNIX-like systems)

    Placeholders available:

    "%CWD%" - the current working directory
    "%HOME%" - the user's home folder

    Returns a fully valid path for the location and system.
    """
    path_steps = path.split("/")
    path = os.path.sep.join(path_steps)
    path = _doSubstitutions(path)

def resolveAll(path_list):
    """ Resolve a list of paths.

    See resolve(path)
    """
    new_path_list = []

    for path in path_list:
        new_path = resolve(path)
        if new_path:
            new_path_list.append(new_path)

    return new_path_list
