#!/usr/bin/env bash

HERE="$(dirname "$0")"
export PYTHONPATH="$HERE"

case "$1" in
    tests/*)
        pytest -s "$1"
        ;;

    python)
        python
        ;;

    *)
        python "$@"
        ;;
esac
