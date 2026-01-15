import argparse
import sys


def parse_args(params=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    action = parser.add_subparsers(dest="action")

    p_reg = action.add_parser("register")
    p_reg.add_argument("path")

    p_hash = action.add_parser("hash")
    p_hash.add_argument("path")

    p_comp = action.add_parser("compare")
    p_comp.add_argument("path1")
    p_comp.add_argument("path2")

    p_merge = action.add_parser("merge")
    p_merge.add_argument("source_dir")
    p_merge.add_argument("dest_dir")
    p_merge.add_argument("--recursive", "-R")

    p_pull = action.add_parser("pull")
    p_pull.add_argument("source_dir")
    p_pull.add_argument("--recursive", "-R")

    p_push = action.add_parser("push")
    p_push.add_argument("dest_dir")
    p_push.add_argument("--recursive", "-R")

    p_flatten = action.add_parser("flatten")
    p_flatten.add_argument("path")

    args = parser.parse_args(params)

    return args
