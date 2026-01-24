import arguments
from dedupe import compare, flatten, merge, registry, ignore, find


def main():
    args = arguments.parse_args()

    if args.action is None:
        arguments.parse_args("-h")

    ignore.load_ignores(args.ignore_file)

    if args.action == "register":
        """ When you expect to have a number of large files to hash
        pre-register the files with this.
        """
        registry.run(args)

    elif args.action == "hash":
        """ Show the hash of a path, _if_ it has been calculated.
        This avoids running a costly checksum if you don't need it.
        """
        registry.get_hash(args)

    elif args.action == "compare":
        """ Informational - see the duplicates
        """
        compare.run(args)

    elif args.action == "merge":
        """ Pull new source dir files into dest dir
        Existing (duplicate) files are left in-place
        """
        for source in args.source_dir:
            merge.do_merge(args.dest_dir, source, args.recursive)

    elif args.action == "push":
        """ Merge current dir files to specified dir
        """
        merge.do_merge(args.dest_dir, ".", args.recursive)

    elif args.action == "pull":
        """ Merge specified dir files files to current dir
        """
        for source in args.source_dir:
            merge.do_merge(".", source, args.recursive)

    elif args.action == "flatten":
        """ Move all deep-nested non-duplicate files down a tree up to the top level directory
        """
        flatten.flatten(args.path)

    elif args.action == "find":
        find.run_find_duplicates(args.path)


if __name__ == "__main__":
    main()
