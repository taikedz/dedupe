import os

import ddexceptions as DDE
#import DedupeDatabase as DDB

class WalkerItem:
    """ Convenience filesystem node representation

    Tracks metadata relevant to the walk
    """

    def __init__(self, path, top_dir):
        if not os.path.islink(path) and not os.path.exists(path):
            raise FileNotFoundError("<%s> does not exist" % path)

        self.path = path
        self.top_dir = top_dir

    def __str__(self):
        return self.getFullPath()

    def getTopDirPath(self):
        """ Return the path of the top directory being processed
        """
        return self.top_dir

    def getFullPath(self):
        """ Get the path name of the file, with the path from the top directory.
        """
        return self.path

    def getName(self):
        """ Get the file name of the current item, without its leading path
        """
        return os.path.basename(self.path)

    def getContents(self, full_paths=False):
        """ Get a listing of files and folders in the folder this WalkerItem represents

        The list is sorted by byte value.

        If full_paths is True, prefixes all content names with the full path of the current item
        """
        contents = os.listdir(self.path)
        contents.sort()
        
        if full_paths:
            contents = ["%s%s%s" % (self.getFullPath(), os.path.sep, child_path) for child_path in contents]

        return contents

    def isdir(self):
        """ Returns True if the item is a directory
        """
        return os.path.isdir(self.path)

    def isfile(self):
        """ Returns True if the item is a file
        """
        return os.path.isfile(self.path)

    def islink(self):
        """ Returns True if the item is a symlink
        """
        return os.path.islink(self.path)

    def registerFile(self):
        raise DDE.NotImplemented("registerFile() not yet implemented")

    def registerAsMeta(self, module_name, flags="", comment=""):
        raise DDE.NotImplemented("registerAsMeta() not yet implemented")
