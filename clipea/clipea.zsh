#!/bin/zsh

if [[ $ZSH_EVAL_CONTEXT != 'toplevel:file' ]]; then
    echo "Error: Source the script instead of executing it:"
    echo
    echo "source $0"
    return 1 2>/dev/null || exit 1
fi

CLIPEA_ARGS="$@"

# wrap in a fn so we don't polute the shell with vars
clipea_init() {
    local CLIPEA_TMP_FILE=$(mktemp)
    local CLIPEA_PYTHON_INTERNAL
    local CLIPEA_PATH_INTERNAL

    # Allow overriding clipea location for development
    # eg CLIPEA_PATH=./clipea source clipea/clipea.zsh
    if [[ -z $CLIPEA_PATH ]]; then
        # default to the installed clipea
        CLIPEA_PATH_INTERNAL=$(builtin which clipea)
    else
        CLIPEA_PATH_INTERNAL=$CLIPEA_PATH
        # only if clipea is overridden then we need to run it with python
        # allow overriding python too
        if [[ -z $CLIPEA_PYTHON ]]; then
            CLIPEA_PYTHON_INTERNAL="$(builtin which python3 || builtin which python)"
        else
            CLIPEA_PYTHON_INTERNAL=$CLIPEA_PYTHON
        fi
    fi

    #echo Debug: $CLIPEA_PYTHON_INTERNAL $CLIPEA_PATH_INTERNAL $CLIPEA_ARGS

    # Execute clipea with an environment variable
    CLIPEA_CMD_OUTPUT_FILE="$CLIPEA_TMP_FILE" $CLIPEA_PYTHON_INTERNAL "$CLIPEA_PATH_INTERNAL" "$CLIPEA_ARGS"

    # Read the command to be placed on the Zsh command line
    COMMAND_TO_PLACE=$(< "$CLIPEA_TMP_FILE")

    # Place it on the Zsh command line
    print -rz "$COMMAND_TO_PLACE"

    rm "$CLIPEA_TMP_FILE"
}
clipea_init

unset CLIPEA_ARGS
