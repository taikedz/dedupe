import argparse
import ddexceptions as dde

def parseArguments(argv):
    argobj = _internalParseArguments(argv)
    _verifyOptions(argobj)
    return argobj

def _verifyOptions(argobj):
    if argobj.walk_only and argobj.resolve:
        raise dde.DDOptionsError("Specify either --walk-only or --resolve, or neither")

    if argobj.resolve and len(argobj.folders) > 0:
        raise dde.DDOptionsError("In resolution-only mode, do not specify folders to walk")

def _internalParseArguments(argv):
    parser = argparse.ArgumentParser(description="Deduplicate files")

    parser.add_argument("-D", "--dbfile", action="store", type=str, default="DedupeDB", help="The database file to store into")
    parser.add_argument("-x", "--delete-from", action="store", type=str, help="File listing names to delete when encountered, one per line")
    parser.add_argument("-i", "--ignore-from", action="store", type=str, help="File listing names to ignore when encountered, one per line")
    parser.add_argument("-r", "--resolve", action='store_true', help="Resolve database only")
    parser.add_argument("-w", "--walk-only", action='store_true', help="Walk folders and build database without resolving")
    parser.add_argument("folders", metavar="FOLDER", nargs="*", help="Folders to check")

    return parser.parse_args(argv)
