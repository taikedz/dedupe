import os
from dedupe import event
from dedupe.db import get_database

# --------------------------------------------------------
# TODO - we'll manually load items here eventually,
# before implementing the dynamic loader
MAIN_DB = None

def ignore_common_files(path:str):
    filename = os.path.basename(path)

    if filename in ["Thumbs.db", ".DS_Store"]:
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
    if os.path.isdir(os.path.join(path, '.git')):
        print(f"Skipping git repo {path}")
        raise event.DedupeSkip(path)
# --------------------------------------------------------

def load_plugins():
    global MAIN_DB
    MAIN_DB = get_database()
    event.register_handler("FILE-FIND", ignore_common_files)
    event.register_handler("FILE-HASH", register_file_path)
    event.register_handler("DIR-FIND", register_git_dir_path)
