import os
import lib.utils
import sys


def get_input() -> str:
    data: str = ""
    if not sys.stdin.isatty():
        data = input()
    if len(data) > 8192:
        exit(
            "Error: Input too long! Maximum 8192 characters allowed. Try limiting your input using 'head -c 8000 file.txt"
        )
    return data


def get_shell() -> str:
    return (
        os.popen("ps -o comm= -p $(ps -o ppid= -p $(ps -o ppid= -p $$))").read().strip()
    )


def execute_with_prompt(cmd: str) -> None:
    answer = input("\033[0;36mExecute? [y/N] \033[0m").strip().lower()
    if answer == "y":
        import subprocess

        subprocess.run(cmd, shell=True)
