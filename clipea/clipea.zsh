#!/bin/zsh

if [[ $ZSH_EVAL_CONTEXT != 'toplevel:file' ]]; then
    echo "Error: Source the script instead of executing it:"
    echo
    echo "source $0"
    return 1 2>/dev/null || exit 1
fi

CLIPEA_TMP_FILE=$(mktemp)

# https://stackoverflow.com/questions/9901210/bash-source0-equivalent-in-zsh
CLIPEA_SCRIPT_DIR=$(dirname $(readlink -f ${(%):-%x}))

CLIPEA_PYTHON=

CLIPEA_PATH=$(builtin which clipea)

# Run clipea from the current dir if possible
if [[ -f $CLIPEA_SCRIPT_DIR/__main__.py ]]; then
    CLIPEA_PATH=$CLIPEA_SCRIPT_DIR
    CLIPEA_PYTHON="$(builtin which python3 || builtin which python)"
fi

# Execute clipea with an environment variable
CLIPEA_CMD_OUTPUT_FILE="$CLIPEA_TMP_FILE" $CLIPEA_PYTHON "$CLIPEA_PATH" "$@"

# Read the command to be placed on the Zsh command line
CLIPEA_COMMAND_TO_PLACE=$(< "$CLIPEA_TMP_FILE")

# Place it on the Zsh command line
print -rz "$CLIPEA_COMMAND_TO_PLACE"

rm "$CLIPEA_TMP_FILE"
