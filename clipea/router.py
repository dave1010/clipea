"""clipea
Base application logic
"""
import sys
from pprint import pprint
from clipea import ENV, USAGE_FILE_PATH, commands, utils


def commands_router(user_prompt: str) -> None:
    """Executes the correct behavior depending on user input

    Args:
        user_prompt (str): user input
    """
    args: list[str] = user_prompt.split()
    if len(args) == 0:
        sys.exit("No query specified")

    match args[0]:
        case "alias":
            commands.alias()
        case "env":
            pprint(ENV)
        case "setup":
            commands.setup()
        case "-h" | "--help" | "help":
            print(utils.read_file(USAGE_FILE_PATH))
        case _:
            commands.clipea_execute_prompt(user_prompt)
