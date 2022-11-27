import os
from dedupe import event
from dedupe.db import get_database

# --------------------------------------------------------
# TODO - we'll manually load items here eventually,
# before implementing the dynamic loader
MAIN_DB = get_database()

def register_file_path(path):
    MAIN_DB.register_path(path)
    return True # indicate that the event was handled

def register_git_dir_path(path):
    if os.path.isdir(os.path.join(path, '.git')):
        raise event.DedupeSkip(path)
# --------------------------------------------------------

def load_plugins():
    event.register_handler("FILE-HASH", register_file_path)
    event.register_handler("DIR-HASH", register_git_dir_path)
