from dedupe import ddargs
from dedupe import plugin
from dedupe.walker import DedupeWalker
from dedupe.db import open_database

def main():
    args = ddargs.parse_args()

    open_database("sqlite3", args.database)

    plugin.load_plugins()


    for dirpath in args.folders:
        walker = DedupeWalker(dirpath)
        walker.walk_folder()


if __name__ == "__main__":
    main()
