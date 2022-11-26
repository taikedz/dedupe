from dedupe import ddargs
from dedupe import event
from dedupe.walker import DedupeWalker


def main():
    args = ddargs.parse_args()

    event.load_handlers()

    walker = DedupeWalker()

    for dirpath in args.folders:
        walker.walk_folder(dirpath)


if __name__ == "__main__":
    main()
