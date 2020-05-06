#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

if [[ -z "$*" ]]; then
    echo -e "$(basename "$0") [FILE | --list | --all | --testfiles]\n\nSpecify a test file to run,\n  or '--list' to list available test files,\n  or '--all' to seek for and test all source files,\n  or '--testfiles' to run all existing test files."

elif [[ "$*" = "--list" ]]; then
    ls test_*.py

elif [[ "$*" = "--testfiles" ]]; then
    for testfile in ./test_*.py ; do
        echo -e "\033[32;1m${testfile}\033[0m"
        bash runtests.sh "$testfile" || :
    done
elif [[ "$*" = "--all" ]]; then
    cd ../dedupe
    while read target_name; do
        [[ "$target_name" != "__init__.py" ]] || continue
        echo -e "\033[32;1m${target_name}\033[0m"
        dir_name="$(dirname "$target_name")"
        base_name="$(basename "$target_name")"
        test_file="../tests_dedupe/$dir_name/test_$base_name"

        if [[ -f "$test_file" ]]; then
            bash ../tests_dedupe/runtests.sh "$test_file" || :
        else
            echo -e "\033[31;1mNo corresponding test file \033[33;1m<$test_file>\033[0m"
        fi
    done < <(find -name '*.py' -type f)
else
    ([[ -f "$1" ]] && [[ "$1" =~ \.py$ ]]) || {
        echo "Specify a test file to run, e.g. 'test_DirWalker.py'"
        exit 1
    }

    PYTHONPATH="${PYTHONPATH:-}:../dedupe:../dedupe/resolvers" python3 "$@"
fi
