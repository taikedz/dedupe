import os

from dedupe import event

class DedupeWalker:

    def process_file(self, file_path):
        if os.path.isfile(file_path):
            print(f"WALKER: Processing file: {file_path}")
            event.execute_handlers("FILE-HASH", file_path)
        else:
            print(f"WALKER: ERROR: !! Could not locate file {file_path}")


    def process_dir(self, dir_path):
        if os.path.isdir(dir_path):
            print(f"WALKER: Processing dir : {dir_path}")
            event.execute_handlers("DIR-HASH", dir_path)
        else:
            print(f"WALKER: ERROR: !! Could not locate dir {dir_path}")


    def walk_folder(self, path):
        print(f"Processing {path}")

        self.process_dir(path)

        for parent_dir, child_dirs, child_files in os.walk(path):
            for file_name in child_files:
                self.process_file(os.path.join(parent_dir, file_name))

            for dir_name in child_dirs:
                self.process_dir(os.path.join(parent_dir, dir_name))