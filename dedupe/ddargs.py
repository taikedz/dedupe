import argparse

def parse_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("folders", nargs="+", help="Folders to traverse")
    parser.add_argument("--database", "-d", default="Dedupe.db")

    return parser.parse_args(args)