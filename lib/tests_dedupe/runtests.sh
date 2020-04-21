#!/usr/bin/env bash

cd "$(dirname "$0")"

([[ -f "$1" ]] && [[ "$1" =~ \.py$ ]]) || {
    echo "Specify a test file to run, e.g. 'test_main.py'"
    exit 1
}

PYTHONPATH="$PYTHONPATH:../dedupe:../dedupe/resolvers" python3 "$@"
