#!/usr/bin/env bash

HERE="$(dirname "$0")"
export PYTHONPATH="$HERE"

case "$1" in
    tests/*)
        pytest -s "$1"
        ;;

    dedupe)
        shift
        python "$HERE/dedupe/dedupe-main.py" "$@"
        ;;

    merge)
        shift
        python "dedupe-tools/dd-merge-dir/main-merge.py" "$@"
        ;;

    lookup)
        shift
        python "dedupe-tools/dd-lookup/dd-lookup.py" "$@"
        ;;
    *)
        echo "Unknown subcommand. Try dedupe/merge/lookup or provide a file in the tests/* dir"
        ;;

esac
