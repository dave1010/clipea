"""CLI
Interactions with the terminal
"""

import readline
import os
import sys
import subprocess
import shutil
from typing import Optional
from loguru import logger as log


def get_input(max_len: int = 1 << 13) -> str:
    """Get user data and do length check on it

    Returns:
        str: user input
    """
    data: str = ""
    if not sys.stdin.isatty():
        data = input()
    if len(data) > max_len:
        raise ValueError(
            f"Error: Input too long! Maximum {max_len} characters allowed.             "
            f"    Try limiting your input using 'head -c {max_len} file.txt"
        )
    return data


def get_current_shell() -> str:
    """Attempts to gets the current shell running
    Returns:
        str: shell's name
    """
    fallback_shell_path = "/bin/sh"  # last resort
    available_shells = [
        "bash",
        "sh",
        "zsh",
    ]
    current_shell = (
        os.popen("ps -o comm= -p $(ps -o ppid= -p $(ps -o ppid= -p $$))").read().strip()
    )
    # If clipea is invoked from a shell script, the `ps` command will return
    # the script that invoked it, not the shell that is running. In this case,
    # we fallback to the preferred user shell, indicated by the env var $SHELL:
    if current_shell not in available_shells:
        current_shell = os.path.basename(os.environ.get("SHELL", fallback_shell_path))
    log.debug(f"Current shell: {current_shell}")
    return current_shell


def find_shell(shell_name: str) -> str | None:
    """Finds the path to the shell passed
    Args:
        shell_name: shell's name
    Returns:
        path to the shell, or None if not found
    """
    if shutil.which(shell_name) is None:
        raise ValueError(f"Error: {shell_name} not found in PATH")
    return shutil.which(shell_name)


def edit_cmd(innacurate_cmd: str) -> str:
    """Lets the user modify a command and returns it."""
    # Set the default text as the pre-fill for readline
    readline.set_startup_hook(lambda: readline.insert_text(innacurate_cmd))

    try:
        # The user can now edit the command and press Enter to submit
        user_approved_cmd = input("Edit, then press ENTER to run:\t")
    finally:
        # Make sure to reset the startup hook so that future uses of
        # raw_input won't have the text inserted.
        readline.set_startup_hook()

    return user_approved_cmd


def execute_after_approval(dirty_cmd: str, shell: Optional[str] = None) -> str | None:
    """Ask user confirmation for running a command or editing it.

    If not an interactive shell (e.g. sourced script), the function does nothing.
    Args:
        cmd (str): command to execute
        shell (str, optional): to execute with a particuliar shell. Defaults to None.
    Returns:
        the command executed (or None) to be added to the history
    """
    # do not run if not an interactive shell
    if not sys.stdin.isatty():
        log.error("Error: clipea is not running in an interactive shell")
        return None

    # confirms with user
    answer = input("\033[0;36mExecute [y/N] or [e]dit? \033[0m").strip().lower()
    answer = "n" if not answer else answer # default is "don't execute"

    # abort if not [y]es or [e]dit
    if answer not in "ye":
        return None

    # enter editing mode if user wants
    approved_cmd = edit_cmd(dirty_cmd) if answer == "e" else dirty_cmd
    subprocess.run(
        approved_cmd,
        shell=True,
        executable=None if shell is None else get_current_shell(),
        check=False,
    )
    return approved_cmd
