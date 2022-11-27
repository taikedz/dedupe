# Deduplicator

Extendable utility to find duplicate files, and tools to resolve duplicates.

Very incomplete. A side project. May never be completed beyond 0.0.1.

## Tree walker

* Background-run utility to walk directory structures to find and identify files
* Extensible via "plugin" handlers for tree-walk events
    * _To bo done ..._
* Ability to ignore files and entire folders during walk (e.g. folder-based projects, git directories, etc)
    * To be improved. See `dedupe/plugins/__init__.py`
* Duplicates information stored to database
* Standalone tool to list duplicates from the database


## Duplication resolution

* Tool for flattening a folder tree to a depth-1 folder
    * _To be implemented..._
* Tool for merging multiple directories into a single base directory, preserving paths
