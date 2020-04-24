import os
import sqlite3

import ddexceptsion as dde

class DuplicatesDatabase:
    def __init__(self, dbfilepath):
        if not os.path.exists(dbfilepath) or os.path.isfile(dbfilepath):
            self.dbpath = dbfilepath
            self.connector = sqlite3.open(dbfilepath)
        else:
            raise dde.DDDatabaseError("%s exists but is not a regular file" % dbfilepath)

    def __registerIdentity(self, filepath, topdir, bsize, part_hash=None, full_hash=None, duplicate=False):
        # Create/update a file identity entry in the database
        pass

    def __lookupIdentity(self, bsize=None, part_hash=None, full_hash=None):
        # Lookup an identity by properties.
        # search on part_hash requires bsize, lookup on full_hash requires only bsize
        pass

    def registerFilePath(self, topdir, filepath):
        # Register a file path in the database
        # Check its bsize and lookup; if entries come back
        #   - if identity has no part hash and is only one file, compute part hash for both files
        #       - update old identity from existing file entry
        #       - if hashes are different, create new identity for current file
        #       - if hashes are the same, proceed to next
        #   - if identity has no full hash and is only one file, or full meta is present, compute full hash for both files
        #       - update old identity from existing file entry, if necessary
        #       - if hashes are different, create new identity for current file
        #       - if hashes are the same, register current file with identity, and mark all files on the identity as duplicate
        #   - register parent directory
        #   - assign parent directory
        #   - return the file entry ID
        pass

    def registerDirPath(self, dirpath):
        # Register directory path if new
        # return the identity ID
        pass

    def listDuplicatesOfPath(self, filepath):
        # Lookup the Identity of the filepath
        # Return list of filepaths for the identity, including the specififed path
        pass

    def getParentOfPath(self, filepath):
        # For a path, get a parent directory entry - return string, the path
        pass
