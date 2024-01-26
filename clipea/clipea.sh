#!/bin/bash -i
# Shell should be interactive to better interact with
#   history e.g. to get the user's $HISTTIMEFORMAT.
set -e

# disable bash history until we're interested in it
history -c
set +o history

CLIPEA_TMP_FILE=$(mktemp)
trap 'rm -f ${CLIPEA_TMP_FILE}' EXIT

# get this script's directory
CLIPEA_SCRIPT_DIR=$(dirname "$0")
CLIPEA_PATH=$(command -v clipea)
CLIPEA_PYTHON=

# run clipea from the current dir if possible
if [[ -f ${CLIPEA_SCRIPT_DIR}/__main__.py ]]; then
    CLIPEA_PATH=${CLIPEA_SCRIPT_DIR}
    CLIPEA_PYTHON=$(command -v python3 || command -v python)
fi

# execute clipea with an environment variable
echo "CLIPEA_TMP_FILE=${CLIPEA_TMP_FILE}"
tail -f "${CLIPEA_TMP_FILE}" &
CLIPEA_CMD_OUTPUT_FILE="${CLIPEA_TMP_FILE}" "${CLIPEA_PYTHON}" "${CLIPEA_PATH}" "$@"

# read the command to be placed on the Bash command line
echo "Saving $(wc -l <"${CLIPEA_TMP_FILE}") command(s) to history"

# re-enable bash history and clear it to only add the relevant parts
set -o history
history -c
while read -r line; do
    history -s "${line}"
done <"${CLIPEA_TMP_FILE}"
