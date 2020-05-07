# Implementation notes

## Files

This program is implemented as a set of Python scripts written with Python 3 in mind

The actual program is in `libs/dedupe` ; the corresponding tests are in `lib/test_dedupe`

The wrapper script in `bin/dedupe` serves two purposes:

* a single point of entry that does not require reworking paths here and there - any path re-jigging is set inside the script on-run, not in the permanent environment at install-time
* the script tries to select the correct python command for cross-platform - on Ubuntu it is simply `python3` but in Fedora this could be `python37` or more generally `python`

The install script places and enables the libs and command files accordingly.

## Tree walk

The tree is walked breadth-first.

Several events are fired, onto which handlers can be attached. Encounter handlers can register themselves against the events, and are fired in registration order.

If a handler is called, it has the option to return either `None` if it took no action, or a `str` message detailing what action was taken. If the processing indicates that no further processing should happen on the item it processed, it should raise a `ProcessorSkipException`, the bahviour for which is defined below

* On entering folder `ON_ENTER_DIR`
    * `ProcessorSkipException` - causes the processor to back out of the directory entirely
* On encountering directory `ON_ENCOUNTER_DIR`
    * `ProcessorSkipException` - causes the processor to not call any more handlers on the directory
* On encountering file `ON_ENCOUNTER_FILE`
    * `ProcessorSkipException` - causes the processor to not call any more handlers on the file

## Encounter handling

To ensure the tree walk remains extendable, we specify separate Encounter handlers.

The default handlers have the following effects, in-order:

* `SymLinkCheck`
    * registered on `ON_ENCOUNTER_DIR`
    * If the directory is a symlink, raise `ProcessorSkipException`
    * The default implementation probably won't deal with symlinks properly
    * This can be configured to be turned off - at user's own peril!

* `IgnoreCheck`
    * registered on `ON_ENCOUNTER_FILE`, `ON_ENCOUNTER_DIR`, to check if a file or folder should be ignored
    * if the file is in the ignore list, raise a `ProcessorSkipException`
        * thus if the file is a folder, do not descend into it

* `DirectoryContentCheck`
    * registered to `ON_ENTER_DIR`, which is the first event on descending into a directory
    * if a configured named directory or file is found at top level of target directory, immediately raises a `ProcessorSkipException` to prevent tinkering with internals of a project directory - e.g. source control, PhotoShop, Kdenlive, etc

* `DeleteCheck`
    * registered on `ON_ENCOUNTER_FILE`, `ON_ENCOUNTER_DIR`, to check if a file or folder should be deleted
    * if the file or folder is in the auto-delete list, remove it, and raise a `ProcessorSkipException`

* `Identify`
    * registered on `ON_ENCOUNTER_FILE`, causing a file to be identified and added to the database
    * if the file is a regular file, register info:
        * top-level specified folder
        * parent path
        * absolute path
        * file size
            * if size already existed, check for small hash
            * if small hash matches, check for full hash
            * if at any stage the entry is not matching, create a new entry with the current stats
    * if a duplicate is found, mark current file and duplicate files with bool

# Resolution handling

To ensure the resolution methods remain extendable, we create separate resolution modules. It should be possible to later add new resolution methods as desired.

## Resolver modules

The following are the intended default modules.

### `DeleteFile`

* Ask which file to keep, or skip, or back
* Delete all other files

### `DeleteDir`

* Obtain all duplicate files' parent directories
    * if a directory is upstream of another directory in the list, a message should be printed and the upstream directory omitted
    * Each directory should appear only once
* Ask which directory to keep, or skip, or back
* Delete all other directories
    * Before deletion, check to see if deletion target is different from, and not upstream from, retention target

### `MergeDir`

* Obtain all duplicate files' parent directories
    * If a candidate merge destination is downstream of another directory, print message, and exclude the downstream directory
    * Each directory should appear only once
* Ask which directory to keep (merge towards), or skip, or back
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
    * Repeat core procedure for subdirectories

# Registering encounter and resolution handlers

A YAML configuration file is specified such. It can be explicitly passed to the program at run time, or implicitly loaded from `dedupe.yaml` in the current working directory, or from a `$HOME/.local/config/dedupe/dedupe.config`, generated during install.

Handlers are declared in the order in which they should be processed. The default settings should generally not be changed - re-ordering them may have unintended consequences.

> WARNING - the following YAML may be incongruent with the current implementation. Please verify.

```yaml

<str> software: should simply be "dedupe" to identify the ownership of the format
<str> version: an X.Y notation version, noting the version of the scheme of the file (not the version of dedupe)

<map> handlers: a list of handler types
    <map> encounters: a list of names of encounter events
        <list> (event name): a list of <str> handler names

    <list> resolutions: a list of pairs: [names of resolution handlers], and [user prompts]

<map> config: a list of handler types
    <map> engine: special config level for the program
        <map> debug: special debug configurations
            <bool> fsdelete: whether to actually perform deleteions in the filesystem
            <bool> dbdelete: whether to perform deletions in the database, mimicking normal-run of deletions (independent of state of `fsdelete`)
    <map> (handler type): an optional entry for each type of handler
        <map> (handler name): each handler can have an entry, with a map of configurations
            <value> (config name): (config value)

---
# Example

software: "dedupe"
version: "0.1"

handlers:
    encounters:
        ON_ENTER_DIR:
            - RepoCheck
        ON_ENCOUNTER_FILE:
            - IgnoreCheck
            - DeleteCheck
            - Identify
        ON_ENCOUNTER_DIR:
            - SymLinkCheck
            - IgnoreCheck
            - DeleteCheck
            - Descend
    resolutions: # user will be reminded that they will select the copy to keep
        - handler: DeleteFile
          prompt: "Remove duplicates"
        - handler: DeleteDir
          prompt: "Delete parent directories"
        - handler: Merge
          prompt: "Merge parent directories"

config:
    engine:
        debug:
            fsdelete: True
            dbdelete: True
        autoskip: False # set to True to bypass prompts and always skip - thus generating a report
    encounters:
        SymLinkCheck:
            follow: False
        ProjectNameCheck: # Simple project folder detection by presence of a dir/file, extenable via config
            dirs:
            - ".git"
            - ".svn"
            files:
            - "*.kdenlive" # Kdenlive projects
            - "*.aup" # Audacity projects
```

# Database

The following is the basic structure of database entries, allowing a decoupling of identities (uniqueness, determined ultimately by hash) and file paths, as well as parent directory paths.

`PRI` denotes a primary key
`EXT` denotes an external key
`IDX` denotes that the column should be indexed, as we expect to search on it

* FileIdentity
    * id : uint / PRI
    * byte_size : uint / long / IDX
    * small_hash : char(32) / IDX
    * full_hash : char(32) / IDX

* FilePath
    * id : uint / PRI
    * path : blob / IDX?
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
