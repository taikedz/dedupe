# Deduplication helper

A lightweight tool to help deduplicate folders of files.

Only processes regular files and folders ; skips symlinks and non-plain-file, non-directory files (e.g. fifo pipes, block devices, etc).

## Store management

Any attempt to query a file, for example during merge or compare, will store the hash and the path. The store can also be explicitly pre-populated with the `register` subcommand.

```sh
# Walk a path and add all files
dedupe register .../path

# Show the hash(es) for the file at the given path, if registered. Only use registry details.
dedupe hash .../path

# Delete the current register
dedupe register %drop
```

## Compare

Compare specified dirs.

By default, this scours just the files of the specified directory, and lists files that have matching hashes

```sh
dedupe compare .../path1 .../path2
```

## Merge

Merge two directories's files. Recurse into subfolders with `-R`

Merging moves files from the source dir to the target dir, if there are no duplicates by hash. Any files ignored for any reason are left in-place.

```sh
# Merge path1 to path2
dedupe merge path1 path2

# Same as `dedupe merge .../path ./`
dedupe pull .../path

# Same as `dedupe merge ./ .../path`
dedupe push .../path
```

## Flatten

Flatten a deep folder tree into a flat folder - that is, bring all files under the folder's tree as direct children of the folder. Leaves duplicate files in-place. Ignore symlinks. Symlinks at top level are checked - if they point to files deep in the folder, these are moved up to top level, else are left alone.

```sh
dedupe flatten .../path
```

```

A layout with N-depth diretories

    maindir
    |
    +-- file1 (hash=abc)
    +-- file2 (hash=def)
    +-- dir1/
        |
        +-- subfile1 (hash=def)
        +-- dir2/dir3/dir4/...
             |
             +-- subfileN (hash=ghi)

Becomes flattened, with hash-duplicates removed.

    maindir
    |
    +-- file1 (hash=abc)
    +-- file2 (hash=def)
    +-- subfileN (hash=ghi)


```

## Ignore

There are two ways to identify a path to ignore: by its name, or by the existence of a particular child path ("beacon" paths) under a directory.

Ignoring affects hash registration as well as comparison and merge. Any ignored items on the source path of a merge is left in place. Ignored items are not registered in the hash database.

### direct names

Before processing a path, its name is checked against the ignore names list. If the path item's basename matches an entry in the `ignore-names` list, that path is not processed.

Example in `~/.dedupe/ignore` file

```
# MacOS filesystem litter
._*
# Some trash folder
.Trash/
```

### beacons

Beacon paths are specified by starting with `./`

On entering any dir, the beacon paths are checked:

* If the current dir has any of the specified paths
* then the whole directory is immediately skipped

Example in `~/.dedupe/ignore` file

```

./.git/
./*.venv/bin/activate
```