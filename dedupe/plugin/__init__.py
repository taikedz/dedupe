import os
from dedupe import event
from dedupe.db import get_database
from dedupe.logger import get_logger

LOG = get_logger("plugin_init")

# --------------------------------------------------------
# TODO - we'll manually load items here eventually,
# before implementing the dynamic loader
MAIN_DB = None

def ignore_common_files(path:str):
    filename = os.path.basename(path)

    if filename in ["Thumbs.db", ".DS_Store", "Desktop.ini"]:
        # We could cure these ills right here and now ...
        #os.remove(path)
        raise event.DedupeSkip(path)

    if filename.endswith(".pyc") or filename.startswith("._"):
        raise event.DedupeSkip(path)


def register_file_path(path):
    MAIN_DB.register_path(path)
    return True # indicate that the event was handled


# Do not try to process a git repo for duplicates
def register_git_dir_path(path):
    path_git_subdir = os.path.join(path, '.git')

    if os.path.isdir(path_git_subdir):
        LOG.info(f"Skipping git repo {path}")
        raise event.DedupeSkip(path)

    else:
        LOG.debug(f"Proceeding with {path} - did not find\n\t{path_git_subdir}")
# --------------------------------------------------------

def load_plugins():
    global MAIN_DB
    MAIN_DB = get_database()
    event.register_handler("FILE-FIND", ignore_common_files)
    event.register_handler("FILE-HASH", register_file_path)
    event.register_handler("DIR-FIND", register_git_dir_path)
