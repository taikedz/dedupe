import os

from dedupe.db import connect_sqlite, DbApi
from dedupe import ddargs
from dedupe import event

class DedupeWalker:

    def __init__(self, DbType, *db_params):
        self.db = DbType(*db_params)


    def process_file(self, file_path):
        if os.path.isfile(file_path):
            print(f" --> {file_path}")
            event.execute_handlers("FILE-HASH")
        else:
            print(f"!! Could not locate file {file_path}")


    def process_dir(self, dir_path):
        if os.path.isdir(dir_path):
            print(f": {dir_path}")
            event.execute_handlers("DIR-HASH")
        else:
            print(f"!! Could not locate dir {dir_path}")


    def dedupe_walk(self, path):
        print(f"Processing {path}")
        for parent_dir, child_dirs, child_files in os.walk(path):
            for file_name in child_files:
                self.process_file(os.path.join(parent_dir, file_name))

            for dir_name in child_dirs:
                self.process_dir(os.path.join(parent_dir, dir_name))


def main():
    args = ddargs.parse_args()

    db = connect_sqlite(args.database)

    for dirpath in args.folders:
        dedupe_walk(dirpath)

if __name__ == "__main__":
    main()
