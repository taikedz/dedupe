#!/usr/bin/env bash

THIS="$(realpath "$0")"
HEREDIR="$(dirname "$THIS")"
SCRIPT="$(basename "$0")"

set -euo pipefail

ensure_venv() {
    local activator="$HEREDIR/.venv/bin/activate"
    (
    [[ -f "$activator" ]] || {
        python3 -m venv "$HEREDIR/.venv/"
        . "$activator"
        pip install -r requirements.txt
    }
    )
    . "$activator"
}

main() {
    ensure_venv

    export PYTHONPATH="$HEREDIR:${PYTHONPATH:-}"
    pytest "$HEREDIR/unittests" "$@"
}

main "$@"
