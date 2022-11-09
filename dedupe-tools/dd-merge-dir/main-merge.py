import argparse
import logging
import os
import shutil

LOG = logging.getLogger()
logging.basicConfig(level=logging.INFO)

CLASH_RESOLVE = None


def main():
    LOG.info("Starting dedupe ...")
    args = parse_arguments()

    if not os.path.isdir(args.main_dir):
        raise OSError(f"{args.main_dir} does not exist.")

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

    return parsed_args


def get_clash_resolve_name(original_name):
    if CLASH_RESOLVE == "skip":
        return None

    elif CLASH_RESOLVE == "force":
        original_name

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
            dest_file = os.path.join(destination_dir, sub_file)

            if not os.path.exists(dest_file):
                shutil.move(sub_file, dest_file)

            elif CLASH_RESOLVE:
                clash_resolved_dest = get_clash_resolve_name(dest_file)
                if clash_resolved_dest:
                    shutil.move(sub_file, clash_resolved_dest)
                else:
                    LOG.info(f"Skipped {sub_file}")

            else:
                message = f"{sub_file} already exists in destination. Use `--resolve RESOLUTION` to provide an action."
                LOG.error(message)
                raise OSError(message)


# =====================
if __name__ == "__main__":
        main()
