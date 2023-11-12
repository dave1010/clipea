import os, sys
import shutil
import lib.cli as cli
import lib.utils as utils
from pathlib import Path

CLIPEA_DIR: str = os.path.dirname(os.path.realpath(__file__))
SYSTEM_PROMPT_FILE: str = CLIPEA_DIR + "/system-prompt.txt"
USAGE_FILE_PATH: str = CLIPEA_DIR + "/usage.txt"
HOME_PATH: str = utils.anystr_force_str(os.path.expanduser("~"))
ENV: dict[str, str] = {
    "shell": cli.get_shell(),
    "os": os.name,
    "editor": os.getenv("EDITOR") or "nano",
}
SYSTEM_PROMPT: str = utils.read_file(SYSTEM_PROMPT_FILE) + str(ENV)

config_path_obj: Path
if (config_path_obj := Path(HOME_PATH + "/.config/clipea/system-prompt.txt")).is_file():
    SYSTEM_PROMPT_FILE = str(config_path_obj)


def commands_router(user_prompt: str) -> None:
    match user_prompt:
        case "alias":
            pass
        case "env":
            from pprint import pprint

            pprint(clipea.ENV)
        case "setup":
            from llm.cli import keys_set

            keys_set()
        case "-h" | "--help" | "help":
            print(utils.read_file(USAGE_FILE_PATH))
        case "":
            exit("No query specified")
        case _:
            from lib.llm import init_llm, stream_commands
            from llm import Model, Response

            data: str = cli.get_input()
            model: Model = init_llm("gpt-4" if user_prompt.startswith("4 ") else "")
            response: Response = model.prompt(
                system=SYSTEM_PROMPT,
                prompt=user_prompt + "~~~DATA~~~" + data,
            )
            print("test")
            stream_commands(response, command_prefix="📎🟢")
