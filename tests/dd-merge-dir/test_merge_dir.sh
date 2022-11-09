#!/usr/bin/env bash

RESULT=0

MAIN_DIR=(
    ./main/this/one.txt
    ./main/this/two.txt
)

SOURCE_DIR=(
    ./sub/one.txt
    ./sub/this/one.txt
)

print_pf() {
    local res="$1"; shift
    if [[ "$res" = 0 ]]; then
        echo "[PASS]" "$*"
    else
        echo "[FAIL]" "$*"
    fi
}

assert_content() {
    local res=0
    [[ "$(cat "$1")" == "$2" ]] || {
        res=1
        RESULT=1
    }

    print_pf $res "$1 contains $2"
}


make_dirs_and_file() {
    local dirname="$(dirname "$1")"
    mkdir -p "$dirname"
    echo "$1" > "$1"
}

setup_environment() {
    for d in "${MAIN_DIR[@]}"; do make_dirs_and_file "$d"; done
    for d in "${SOURCE_DIR[@]}"; do make_dirs_and_file "$d"; done
}

# =======

setup_environment

(set -x
python3 ./dedupe-tools/dd-merge-dir/main-merge.py -r force main sub
)

assert_content ./main/this/one.txt ./sub/this/one.txt
assert_content ./main/this/two.txt ./main/this/two.txt
assert_content ./main/one.txt ./sub/one.txt
assert_content <(set -x; find sub -type f|wc -l) 0

rm -r ./main ./sub

echo "========"

setup_environment

(set -x
python3 ./dedupe-tools/dd-merge-dir/main-merge.py -r rename main sub
)

assert_content ./main/this/one.txt ./main/this/one.txt
assert_content ./main/this/one.txt-1 ./sub/this/one.txt
assert_content ./main/this/two.txt ./main/this/two.txt
assert_content ./main/one.txt ./sub/one.txt
assert_content <(set -x; find sub -type f|wc -l) 0

rm -r ./main ./sub

echo "========"

setup_environment

(set -x
python3 ./dedupe-tools/dd-merge-dir/main-merge.py -r skip main sub
)

assert_content ./main/this/one.txt ./main/this/one.txt
assert_content ./sub/this/one.txt ./sub/this/one.txt
assert_content ./main/this/two.txt ./main/this/two.txt
assert_content ./main/one.txt ./sub/one.txt
assert_content <(set -x; find main -type f|wc -l) 3
assert_content <(set -x; find sub -type f|wc -l) 1

rm -rf sub main
echo "========"

print_pf $RESULT

exit $RESULT
