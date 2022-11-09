# Implementation notes

## Tree walk

The tree walk is the core operation for finding files. It proceeds fairly simply:

* For a given directory, list its immediate child files and folders
* For each file, execute the handler suite registered to an event `FILE_HASH`
    * The handlers take care of identifying the file, or determining the need to skip it
* Then for each folder, perform the same on `DIR_HASH` event's handlers

## Events

Each named event can have a handler registered to it. By default, this utility provides base handlers for deriving a meaningful hash for the file.

Additional handlers can be supplied to, for example, identify a git folder and cause the folder to be skipped entirely.

## Duplicates identification

Each file processed by the default handler will be registered to the database with its exact byte-size.

If another file is found to have a matching byte-size, a short hash for the first N bytes of each file is produced, and the comparison is performed again. If the short hashes match, then the full hash of each file is produced. If those match, the file is deemed to be a duplicate.

Any file (including a folder) can produce a hash. The registered hash may not necessarily be a strict hash, but an arbitrary string identifying the item.