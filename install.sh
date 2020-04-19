#!/usr/bin/env bash

set -euo pipefail

LIBPATH="/usr/local/lib"
BINPATH="/usr/local/bin"

# ======

cd "$(dirname "$0")"

confirmuser() {
    read -p "Installing as $1 - proceed? y/N> "
    if [[ "$REPLY" =~ ^(n|N|no|NO)$ ]]; then
        echo Abort
        exit 1
    fi
}

if [[ "$UID" = 0 ]]; then
    confirmuser root
else
    confirmuser "$(whoami)"
fi

if [[ "$UID" != 0 ]]; then
    LIBPATH="$HOME/.local/lib"
    BINPATH="$HOME/.local/bin"
    mkdir -p "$LIBPATH"
    mkdir -p "$BINPATH"

    if [[ ! "$PATH" =~ "$HOME/.local/bin" ]]; then
        echo "export PATH=\"\$PATH:$BINPATH\"" >> "$HOME/.bashrc"
        echo "Added '$BINPATH' to your \$PATH ; start a new shell with \`exec bash\` for this to take effect."
    fi
fi

rsync -a "./lib/dedupe/" "$LIBPATH/dedupe/"
sed -e "s|%LIBPATH%|$LIBPATH|"  "./bin/dedupe" > "$BINPATH/dedupe"
