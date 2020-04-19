# Implementation notes

## Tree walk

For each folder provided, descend and

* if the file is in the ignore list, skip it
    * if the file is a folder, do not descend into it
* if the file is in the auto-delete list, remove it
    * if the file is a folder, confirm (y/n/always/never)
    * always/never applies to that filename only

* if the file is a regular file, register info
    * top-level specified folder
    * parent path
    * absolute path
    * file size
        * if size already existed, check for small hash
        * if small hash matches, check for full hash
        * if at any stage the entry is not matching, create a new entry with the current stats
* if a duplicate is found, mark current file and duplicate files with bool

## Resolution

* Offer to delete files
* Offer to delete directories
* Offer to merge

### Deletion

* Ask which file to keep
* or ask which directory to keep
    * additional confirmation if there are subdirectories
        * keep all
        * delete files but not folders
        * delete all

### Merge

* Obtain all duplicate files' parent directories
* Ask which directory to keep (merge towards)
* Ask whether to operate recursively
* Core procedure
    * Obtain all the files in the destination directory
    * For each source duplicates directory
        * Obtain all files in the file's parent directory
        * Check that the file does not already exist in the destination directory, by identity
        * Copy any file that does not already exist
            * remove after checking from source location
            * remove database entry
        * Check each destination file, see if it still has actual duplicates
            * if not, set boolean accordingly
* If operating recursively, for each source folder
    * Repeat core procedure

## Database

The following is the basic structure of database entries, allowing a decoupling of identities (uniqueness, determined ultimately by hash) and file paths, as well as parent directory paths.

`PRI` denotes a primary key
`EXT` denotes an external key
`IDX` denotes that the column should be indexed, as we expect to search on it

* FileIdentity
    * id : uint / PRI
    * byte_size : uint / long / IDX
    * small_hash : char(64) / IDX
    * full_hash : char(64) / IDX

* FilePath
    * id : uint / PRI
    * path : blob
    * top_path : uint / EXT
    * parent_path : uint / EXT
    * identity : uint / EXT
    * duplicate : bool

* ParentPath
    * id : uint / PRI
    * path : blob

### Repairing the database

If some inconsistency is suspected in the database, it can be repaired naively as follows:

* For each FileIdentity
* Check for associated FilePath
    * If none, delete the identity
    * If several
        * Check if any paths match, remove duplicate paths
    * If still several
        * Check the identity has a `full_hash`
        * If not, check each file and associate identities properly, creating new ones if needed
    * If still several, mark all FilePath `duplicate` boolean

This does not guarantee consistency with the filesystem. A rebuild would need to build the database up from scratch...
