import os

from dedupe import event

class DedupeWalker:

    def __init__(self, base_path):
        self.skip_paths = []
        self.base_path = base_path


    def process_file(self, file_path):
        if os.path.isfile(file_path):
            event.execute_handlers("FILE-FIND", file_path)
            print(f"WALKER: Processing file: {file_path}")
            event.execute_handlers("FILE-HASH", file_path)
        else:
            print(f"WALKER: ERROR: !! Could not locate file {file_path}")


    def process_dir(self, dir_path):
        if os.path.isdir(dir_path):
            event.execute_handlers("DIR-FIND", dir_path)
            print(f"WALKER: Processing dir : {dir_path}")
            event.execute_handlers("DIR-HASH", dir_path)
        else:
            print(f"WALKER: ERROR: !! Could not locate dir {dir_path}")


    def parent_was_skipped(self, path:str):
        for skipped in self.skip_paths:
            if path.startswith(skipped):
                return True

        return False


    def walk_folder(self):
        print(f"Processing {self.base_path}")

        self.process_dir(self.base_path)

        for parent_dir, child_dirs, child_files in os.walk(self.base_path):
            if self.parent_was_skipped(parent_dir):
                # Do not process anything in here if we are inside a skipped dir
                continue

            try:
                for file_name in child_files:
                    self.process_file(os.path.join(parent_dir, file_name))

                for dir_name in child_dirs:
                    self.process_dir(os.path.join(parent_dir, dir_name))

            except event.DedupeSkip as e:
                self.skip_paths.append(e.path)
