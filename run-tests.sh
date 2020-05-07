#!/usr/bin/env sh

cd "$(dirname "$0")"

bash lib/tests_dedupe/runtests.sh "$@"
