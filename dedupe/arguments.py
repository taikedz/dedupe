import argparse
import sys

from dedupe import config


def parse_args(params=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--registry-file", default=config.GLOBAL_REGISTRY, help=f"Location of registry file to use. Default {config.GLOBAL_REGISTRY}")
    parser.add_argument("--ignore-file", default=config.IGNORE_FILE, help=f"Location of ignore file to use. Default {config.IGNORE_FILE}")

    action = parser.add_subparsers(dest="action")

    p_reg = action.add_parser("register")
    p_reg.add_argument("path")

    p_hash = action.add_parser("hash")
    p_hash.add_argument("path")

    p_comp = action.add_parser("compare")
    p_comp.add_argument("path1")
    p_comp.add_argument("path2")

    p_merge = action.add_parser("merge")
    p_merge.add_argument("dest_dir")
    p_merge.add_argument("source_dir", nargs="+")
    p_merge.add_argument("--recursive", "-R", action="store_true")

    p_pull = action.add_parser("pull")
    p_pull.add_argument("source_dir", nargs="+")
    p_pull.add_argument("--recursive", "-R", action="store_true")

    p_push = action.add_parser("push")
    p_push.add_argument("dest_dir")
    p_push.add_argument("--recursive", "-R", action="store_true")

    p_flatten = action.add_parser("flatten")
    p_flatten.add_argument("path")

    p_find = action.add_parser("find")
    p_find.add_argument("path")

    args = parser.parse_args(params)

    config.GLOBAL_REGISTRY = args.registry_file
    config.IGNORE_FILE = args.ignore_file

    return args
