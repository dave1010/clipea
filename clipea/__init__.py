"""Clipea application
📎🟢 Like Clippy but for the CLI. A blazing fast AI helper for your command line
"""
import os
import sys
from clipea import utils, cli


CLIPEA_DIR: str = os.path.dirname(os.path.realpath(__file__))
USAGE_FILE_PATH: str = CLIPEA_DIR + "/usage.txt"
HOME_PATH: str = utils.anystr_force_str(os.path.expanduser("~"))
SYSTEM_PROMPT_FILE: str = utils.get_config_file_with_fallback(
    home=HOME_PATH, fallback=CLIPEA_DIR, appname="clipea", filename="system-prompt.txt"
)
ENV: dict[str, str] = {
    "shell": cli.get_shell(),
    "platform": sys.platform,
    "editor": os.getenv("EDITOR", "nano"),
}
SYSTEM_PROMPT: str = utils.read_file(SYSTEM_PROMPT_FILE) + str(ENV)
