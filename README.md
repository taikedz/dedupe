# Deduplicator

Extendable utility to find duplicate files, and offer a resolution path.

## Features

* Command-based, batch-programmable duplicates identifier
* Extensible -  written with extension in mind via its handlers.
* Directory walking powered by event-driven pre-processing handlers
    * SymLink Check - ignores symlinks. A limitation of the implememntation
    * Ignore - provide a list of file and directory names to ignore, like `__pycache__` directories and `*.pyc` files. Takes precedence over auto-deletion.
    * Auto-deletion - provide list of file and directory names to automatically delete during analysis, such as `Thumbs.db` and `.DS_Store` files.
    * Repository/project folder detection - detect Git and SVN repositories, and exclude from analysis (extendable to general project folder detection, via config)
* Duplicates-resolution handlers:
    * Delete invidivdual files
    * Delete directories where duplicates are found
    * Merge parent directories of files - consolidate files and folders from source folder where duplicates are found to a destination folder, then delete source folder
    * Skip altogether
* Save duplicates information into a database file for staged work sessions and custom analysis
    * SQLite primary target

## Usage

```sh
dedupe [--database DBFILE] [--config CONFIGFILE] [--delete-from LISTFILE] [--ignore-from LISTFILE] [--resolve|--walk-only [--dump] ] [FOLDERS ...]
```

* `--database DBFILE` or `-D DBFILE` - specify the database file to store information in (default file is "./dedupe.sqlite")
* `--config CONFIGFILE` - specify a custom configuration file
* `--resolve` - only resolve the database. Specifying folders would cause an error
* `--walk-only` - only walk the folders to build the database, do not progress to ask for resolution
    * folders must be specified
    * `--dump` - dump the list of duplicates found
