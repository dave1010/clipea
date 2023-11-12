"""CLI
Interactions with the terminal
"""
import os
import sys
import subprocess
import shutil


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
            f"Error: Input too long! Maximum {max_len} characters allowed.\
                 Try limiting your input using 'head -c {max_len} file.txt"
        )
    return data


def get_shell() -> str:
    """Get user's default shell

    Returns:
        str: shell's name
    """

    return (
        os.popen("ps -o comm= -p $(ps -o ppid= -p $(ps -o ppid= -p $$))").read().strip()
    )


def execute_with_prompt(cmd: str, shell: str = None) -> None:
    """Asks the user if he wants to execute a command, executes it if so

    Args:
        cmd (str): command to execute
        shell (str, optional): to execute with a particuliar shell. Defaults to None.
    """
    answer = input("\033[0;36mExecute? [y/N] \033[0m").strip().lower()
    if answer == "y":
        subprocess.run(cmd, shell=True, executable=shutil.which(shell), check=False)
