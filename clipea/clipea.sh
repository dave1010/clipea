#!/bin/bash -i
# Bash integration script for Clipea.
# This file should remain with the Python implementation.

# Shell should be interactive to better interact with
#   history e.g. to get the user's $HISTTIMEFORMAT.
set -e

# enable debug if --debug is passed
if [[ "$1" == "--debug" ]]; then
    IS_DEBUG=1
    shift
else
    IS_DEBUG=${IS_DEBUG:-0}
fi

# disable bash history until we're interested in it
history -c
set +o history

CLIPEA_TMP_FILE=$(mktemp)
# trap '/bin/rm -f ${CLIPEA_TMP_FILE}' EXIT

# get this script's directory
CLIPEA_SCRIPT_DIR=$(dirname "$0")
CLIPEA_PATH=$(command -v clipea)
CLIPEA_PYTHON=

# run clipea from the current dir if possible
if [[ -f ${CLIPEA_SCRIPT_DIR}/__main__.py ]]; then
    CLIPEA_PATH=${CLIPEA_SCRIPT_DIR}
    CLIPEA_PYTHON=$(command -v python3 || command -v python)
fi

# check IS_DEBUG
if [[ ${IS_DEBUG} -eq 1 ]]; then
    echo "CLIPEA_TMP_FILE=${CLIPEA_TMP_FILE}"
    tail -f "${CLIPEA_TMP_FILE}" &
fi

# execute clipea with an environment variable
CLIPEA_CMD_OUTPUT_FILE="${CLIPEA_TMP_FILE}" "${CLIPEA_PYTHON}" "${CLIPEA_PATH}" "$@"

# read the command to be placed on the Bash command line
num_lines_to_save=$(grep -cv '^$' "${CLIPEA_TMP_FILE}")
if [[ ${IS_DEBUG} -eq 1 ]]; then
    echo "Saving ${num_lines_to_save} command(s) to history"
    cat "${CLIPEA_TMP_FILE}"
fi

# re-enable bash history and clear it to only add the relevant parts
set -o history
history -c
while read -r line; do
    if [[ -n "${line}" ]]; then
        history -s "${line}"
    fi
done <"${CLIPEA_TMP_FILE}"
