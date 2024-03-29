#!/usr/bin/env puython3

"""
Directory Merge Tool

Part of taikedz's dedupe suite

---

Tool for merging multiple directories' contents into a single target base directory.
The paths inside the source directories are retained in their copy-overs to the
 target directory.

---
(C) Tai Kedzierski, released under GPLv3
"""

import argparse
import logging
import os
import shutil

LOG = logging.getLogger()
logging.basicConfig(level=logging.INFO)

CLASH_RESOLVE = None

class DDMWalkError(OSError): pass


def main():
    LOG.info("Starting dedupe ...")
    args = parse_arguments()

    if not os.path.isdir(args.main_dir):
        raise DDMWalkError(f"{args.main_dir} does not exist.")

    for src_dir in args.source_dirs:
        walk_and_merge(args.main_dir, src_dir)


def parse_arguments(args=None):
    global CLASH_RESOLVE

    clash_resolutions = ["skip", "force", "rename"]

    parser = argparse.ArgumentParser()
    parser.add_argument("main_dir")
    parser.add_argument("source_dirs", nargs="+")
    parser.add_argument("--resolve-clash", "-r", choices=clash_resolutions, default=None)

    parsed_args = parser.parse_args(args)

    CLASH_RESOLVE = parsed_args.resolve_clash

    return parsed_args


def get_clash_resolve_name(original_name):
    if CLASH_RESOLVE == "skip":
        return None

    elif CLASH_RESOLVE == "force":
        return original_name

    elif CLASH_RESOLVE == "rename":
        i = 0
        new_name = original_name

        while os.path.exists(new_name):
            i += 1
            new_name = f"{original_name}-{i}"
        
        return new_name


def walk_and_merge(destination_dir, source_path):
    for nested_base, _nested_dirs, nested_files in os.walk(source_path):
        for nested_f in nested_files:
            sub_file  = os.path.join(nested_base, nested_f)
            inner_path = os.path.sep.join(sub_file.split(os.path.sep)[1:])
            dest_file = os.path.join(destination_dir, inner_path)

            if not os.path.exists(dest_file):
                # File does not exist, maybe parent dirs don't exist either
                interim_dir = os.path.sep.join(inner_path.split(os.path.sep)[:1])
                interim_dir = os.path.join(destination_dir, interim_dir)

                if not os.path.isdir(interim_dir):
                    os.makedirs(interim_dir)

                shutil.move(sub_file, dest_file)

            elif CLASH_RESOLVE:
                clash_resolved_dest = get_clash_resolve_name(dest_file)
                if clash_resolved_dest:
                    LOG.debug(f"Clash-resolve: Moving {sub_file} -> {clash_resolved_dest}")
                    shutil.move(sub_file, clash_resolved_dest)
                else:
                    LOG.info( f"Clash-resolve: Skipped {sub_file}")

            else:
                message = f"Clash-resolve: {inner_path} already exists in destination. Use `--resolve RESOLUTION` to provide an action."
                LOG.error(message)
                raise DDMWalkError(message)


# =====================
if __name__ == "__main__":
        main()
