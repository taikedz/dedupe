#!/usr/bin/env bash

THIS="$(realpath "$0")"
HEREDIR="$(dirname "$THIS")"
SCRIPT="$(basename "$0")"

set -euo pipefail

main() {
    set -x
    mkdir -p "$HOME/.local/bin"
    ln -s "$HEREDIR/dedupe.sh" "$HOME/.local/bin/dedupe"
    : "Done"
}

main "$@"
