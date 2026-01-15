"""
Given a folder, recurse down and add to a "dedupe.sqlite" file at top level
Ignore any `dedupe.sqlite` files systematically

Once all files added, query database for all paths that have a full-hash.

Get all full hashes, reduce to unique

For each hash, query database for paths
"""