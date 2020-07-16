import os
import platform

_subtitutes = {
    "%CWD%" : os.getcwd(),
    "%HOME%" : os.path.expanduser("~"),
    "%DATA%" : ".local/lib"
}

if platform.system() == "Windows":
    _substitutes["%DATA%"] = "AppData/Roaming"

global_config_paths = [
    "%CWD%/Dedupe.yaml",
    "%HOME%/%DATA%/dedupe/Dedupe.yaml",
]

def _doSubstitutions(path):
    for sub in _substitutes.keys():
        path = path.replace(sub, _substitutes[sub])
    return path

def resolve(path):
    """ Resolve a path.

    Paths are expressed as UNIX-style paths (with '/' separator), and can have placeholders.

    This function replaces elements as appropriate, as well as converting to the local mode of expression of path separators
    (different between Windows and UNIX-like systems)

    Placeholders available:

    "%CWD%" - the current working directory
    "%HOME%" - the user's home folder
    "%DATA%" - the overall folder for a user's application data

    Returns a fully valid path for the location and system.
    """
    path = _doSubstitutions(path)
    path_steps = path.split("/")
    path = os.path.sep.join(path_steps)

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
