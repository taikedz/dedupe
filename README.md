# Deduplicator

Utility to find duplicate files.

Features:

* Save duplicates information into a database file for re-use and staged work
* Resolution actions:
    * Delete invidivdual files
    * Delete directories where duplicates are found
    * Merge parent directories of files - consolidate files and folders from source folder where duplicates are found to a destination folder, then delete source folder
* Ignore - provide a list of filenames to ignore, like `.git`. Takes precedence over auto-deletion
* Auto-deletion - provide list of filenames to automatically delete during analysis, such as `Thumbs.db` and `.DS_Store` files

## Usage

```sh
dedupe --database DBFILE [--delete-from LISTFILE] [--ignore-from LISTFILE] [--resolve|--walk-only [--dump] ] [FOLDERS ...]
```

* `--database DBFILE` or `-D DBFILE` - specify the database file to store information in (required)
* `--delete-from LISTFILE` - a text file with a list of names to automatically delete, one per line
* `--ignore-from LISTFILE` - a text file with a list of names to ignore, one per line
* `--resolve` - only resolve the database. Specifying folders would cause an error
* `--walk-only` - only walk the folders to build the database, do not progress to ask for resolution
    * folders must be specified
    * `--dump` - dump the list of duplicates found
