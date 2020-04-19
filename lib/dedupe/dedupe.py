import sys

import ddargparse
import ddexceptions as dde


def main():
    try:
        argobj = ddargparse.parseArguments(sys.argv)
        print(dir(argobj))
    except dde.DDOptionsError as e:
        e.terminate()

if __name__ == "__main__":
    main()
