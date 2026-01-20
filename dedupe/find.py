"""
Find all existing duplicates under a given path

Given a folder, recurse down and add to registry

Once all files added, query database for all paths that have a full-hash.

Get all full hashes, reduce to unique

For each hash, query database for paths
"""
