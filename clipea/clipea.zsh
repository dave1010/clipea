#!/bin/zsh

if [[ $ZSH_EVAL_CONTEXT != 'toplevel:file' ]]; then
    echo "Error: Source the script instead of executing it:"
    echo
    echo "source $0"
    return 1 2>/dev/null || exit 1
fi

DIR="$(dirname -- "$0")"

TMP_FILE=$(mktemp)

# Execute the PHP script with an environment variable
CLIPEA_CMD_OUTPUT_FILE="$TMP_FILE" "$(which clipea)" "$@"

# Read the command to be placed on the Zsh command line
commandToPlace=$(< "$TMP_FILE")

# Place it on the Zsh command line
print -rz "$commandToPlace"

# Remove the temp file
rm "$TMP_FILE"
