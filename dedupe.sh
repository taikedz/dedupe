#!/usr/bin/env bash

HERE="$(dirname "$(readlink -f "$0")")"

PYTHONPATH="$HERE" python3 "$HERE/dedupe/main.py" "$@"
