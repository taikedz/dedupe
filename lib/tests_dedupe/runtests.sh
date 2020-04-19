#!/usr/bin/env bash

([[ -f "$1" ]] && [[ "$1" =~ \.py* ]]) || {
    echo "Specify a test file to run, e.g. 'test_main.py'"
    exit 1
}

PYTHONPATH="$PYTHONPATH:../dedupe" python3 "$@"
