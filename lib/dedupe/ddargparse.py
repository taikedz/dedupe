import sys
import argparse

def parseArguments():

    parser = argparse.ArgumentParser(sys.argv, description="Deduplicate files")

    parser.add_argument("-D", "--dbfile", action="store", type=str, default="DedupeDB", help="The database file to store into")
    parser.add_argument("-x", "--delete-from", action="store", type=str, help="File listing names to delete when encountered, one per line")
    parser.add_argument("-i", "--ignore-from", action="store", type=str, help="File listing names to ignore when encountered, one per line")
    parser.add_argument("-r", "--resolve", action='store_true', help="Resolve database only")
    parser.add_argument("-w", "--walk-only", action='store_true', help="Walk folders and build database without resolving")
    parser.add_argument("folders", metavar="FOLDER", nargs="*", help="Folders to check")

    return parser.parse_args()

parseArguments()
