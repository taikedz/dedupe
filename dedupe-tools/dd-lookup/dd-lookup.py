# Extremely janky code for querying the dulicates dtabase
# In dire need of a cleanup

import json
import os
import sqlite3
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--database", "-d", default="Dedupe.db")

    subp = parser.add_subparsers(dest="cmd")

    cmd_path = subp.add_parser("path", help="Display duplicate paths given a path")
    cmd_path.add_argument("path", help="Path to check duplicates for")

    cmd_hash = subp.add_parser("hash", help="Display duplicate paths given a hash")
    cmd_hash.add_argument("hash", help="Hash to check duplicates for")

    cmd_info = subp.add_parser("info", help="Check info for a given path")
    cmd_info.add_argument("path", help="Path to check info for")

    subp.add_parser("list", help="list all duplicates hashes")


    subp.add_parser("list-all", help="list all duplicates hashes, and their corresponding paths")

    return parser.parse_args(args)


def main():
    args = parse_args()
    db = sqlite3.connect(args.database)
    cursor = db.cursor()

    # TO DO - jsonify the rest of the outputs

    def list_hash_duplicates(hash):
        entries = [x for x in cursor.execute("SELECT path FROM Paths WHERE full_hash=?", (hash,))]
        [row[0] for row in entries]

    def get_duplicate_hashes():
        return [x[0] for x in cursor.execute("SELECT full_hash FROM Duplicates")]


    if args.cmd == "path":
        path = os.path.abspath(args.path)
        path_hash_set = [x for x in cursor.execute("SELECT full_hash FROM Paths WHERE path=?", (path,))]
        if path_hash_set and path_hash_set[0][0]:
            [print[x] for x in list_hash_duplicates(path_hash_set[0][0])]

    elif args.cmd == "hash":
        [print[x] for x in list_hash_duplicates(args.hash)]

    elif args.cmd == "list":
        [print(h) for h in get_duplicate_hashes()]

    elif args.cmd == "list-all":
        dupe_hashes = get_duplicate_hashes()

        for hash in dupe_hashes:
            # print a comment line, then a JSON dump
            print(f"# HASH   {hash}")
            json_obj = {"hash": hash}
            json_obj["paths"] = list_hash_duplicates(hash)
            print(json.dumps(json_obj))
            print("")

    elif args.cmd == "info":
        path = os.path.abspath(args.path)
        path_hash_set = [x for x in cursor.execute("SELECT path,size,short_hash,full_hash FROM Paths WHERE path=?", (path,))]
        if path_hash_set:
            print(json.dumps({
                "path":{path_hash_set[0][0]},
                "size":{path_hash_set[0][1]},
                "short_hash":{path_hash_set[0][2]},
                "full_hash":{path_hash_set[0][3]},
            }))


if __name__ == "__main__":
    main()
