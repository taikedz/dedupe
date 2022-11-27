""" Basic utility to create temporary testing directory structures

Specify a yaml structure of folder hierarchies.

```yaml
top_dir_name:
    next_dir_name:
        file_name: if an entry has a string content, it is a file

topfile_name: several entries can exist at top level

top_file_name_2: like so
```

Pass this YAML string into `TempFilesystem(yaml_str)` to create the corresponding structure and data.

Call the TempFilesystem instance's `cleanup()` to remove the files as per the spec

"""

import os
import yaml
from shutil import rmtree
from io import StringIO
from typing import Dict, List


class TempFilesystem:

    def __init__(self, fs_yaml):
        self.fs_dict = yaml.safe_load(StringIO(fs_yaml))
        self.make_temp_structure(self.fs_dict)


    def make_temp_structure(self, folder_structure:Dict, parent:List=None):
        if parent is None: parent = []

        for k, v in folder_structure.items():
            full_path = parent[:]+[k]
            if isinstance(v, str):
                with open(os.path.sep.join(full_path), 'w') as fh:
                    fh.write(v)
                    fh.write("\n")

            else:
                os.makedirs(os.path.sep.join(full_path))
                if v is not None:
                    self.make_temp_structure(v, full_path)


    def cleanup(self):
        top_names = self.fs_dict.keys()

        for name in top_names:
            if os.path.isdir(name):
                rmtree(name)

            else:
                os.remove(name)
