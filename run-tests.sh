#!/usr/bin/env sh

export PYTHONPATH="$PYTHONPATH:$(dirname "$0")/lib/tests_dedupe"

cd "$(dirname "$0")"

bash lib/tests_dedupe/runtests.sh "$@"
