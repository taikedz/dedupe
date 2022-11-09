# Deduplicator

Extendable utility to find duplicate files, and tools to resolve duplicates.

## Tree walker

* Background-run utility to walk directory structures to find and identify files
* Extensible via "plugin" handlers for tree-walk events
* Ability to ignore files and entire folders during walk (e.g. folder-based projects, git directories, etc)
* Duplicates information stored to database
* Standalone tool to list duplicates from the database


## Duplication resolution

* Tool for flattening a folder tree to a depth-1 folder
* Tool for merging multiple directories into a single base directory, preserving paths