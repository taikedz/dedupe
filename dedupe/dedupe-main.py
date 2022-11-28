from dedupe import ddargs
from dedupe import plugin
from dedupe.walker import DedupeWalker
from dedupe.db import open_database
from dedupe.logger import remove_log_dir

def remove_logs_folder(remove=False):
    if remove:
        remove_log_dir()


def main():
    args = ddargs.parse_args()

    remove_logs_folder(args.remove_logs)

    # TODO - dynamically select database connector
    open_database("sqlite3", args.database)

    plugin.load_plugins()


    for dirpath in args.folders:
        walker = DedupeWalker(dirpath)
        walker.walk_folder()


if __name__ == "__main__":
    main()
