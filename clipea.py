import os, sys
import shutil
import lib.cli as cli
import lib.utils as utils
from pathlib import Path

CLIPEA_DIR: str = os.getcwd()
SYSTEM_PROMPT_FILE: str = CLIPEA_DIR + "/system-prompt.txt"
USAGE_FILE: str = CLIPEA_DIR + "/usage.txt"
HOME_PATH: str = utils.anystr_force_str(os.path.expanduser("~"))
ENV: dict[str, str] = {
    "shell": cli.get_shell(),
    "os": os.name,
    "editor": os.getenv("EDITOR") or "nano",
}

config_path_obj: Path
if (config_path_obj := Path(HOME_PATH + "/.config/clipea/system-prompt.txt")).is_file():
    SYSTEM_PROMPT_FILE = str(config_path_obj)


system_prompt:str = utils.read_file(SYSTEM_PROMPT_FILE)
system_prompt += str(ENV)

user_prompt = " ".join(sys.argv[1:])

match user_prompt:
    case ("alias"):
        pass
    case "env":
        from pprint import pprint

        pprint(ENV)
        exit()
    case "setup":
        pass
    case "-h" | "--help" | "help":
        with open(CLIPEA_DIR + "/usage.txt") as f:
            print(utils.anystr_force_str(f.read()))
        exit()
    case "":
        exit("No query specified")

if shutil.which("llm"):
    exit("Error: dependency 'llm' not found. Run 'clipea setup' to install")

data: str = cli.get_input()
