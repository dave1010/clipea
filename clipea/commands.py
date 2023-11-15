"""Commands
Commands with a bit more logic than a few lines are stored there
"""
import sys
import json
from clipea import ENV, SYSTEM_PROMPT, CLIPEA_DIR, cli


def setup():
    """Checks if `llm` has an openai key and prompt to change it or create one"""
    import llm.cli

    should_setup = True
    path = llm.cli.user_dir() / "keys.json"
    if path.exists():
        keys = json.loads(path.read_text())
        should_setup = "openai" not in keys.keys()

    if should_setup:
        print(
            "Get an OpenAI API key from: https://platform.openai.com/account/api-keys"
        )
    else:
        print("An OpenAI key is already set-up, proceed if you want to change it.")
    llm.cli.keys_set()  


def clipea_execute_prompt(user_prompt: str):
    """Clipea's logic on prompt.
    Structure all user input as so:

    <user_input>
    ~~~DATA~~~
    <data>

    Sends it to `llm`, stream the responses and prompt if the user wants
    to execute them. If zsh extension is enabled, it will be put into
    zsh's buffer

    Args:
        user_prompt (str): user command input
    """
    from clipea import clipea_llm
    from llm import Model, Response

    llm_name:str = ''
    if user_prompt.startswith('4 '):
        user_prompt = user_prompt[2:]
        llm_name = 'gpt-4'

    try:
        model: Model = clipea_llm.init_llm(llm_name)
    except Exception as e:
        sys.exit(str(e))

    user_data: str = cli.get_input()
    response: Response = model.prompt(
        system=SYSTEM_PROMPT,
        prompt=user_prompt + (("\n~~~DATA~~~\n" + user_data) if user_data else ""),
    )
    clipea_llm.stream_commands(response, command_prefix="📎🟢")


def alias():
    """Gives zsh's alias (automatic command buffering) commands to the user"""
    shell: str = ENV["shell"]
    if shell == "zsh" or shell == "-zsh":
        command: str = f"alias '??'='source {CLIPEA_DIR}/clipea.zsh'"
        user_prompt: str = f"Append this line to my {shell} startup file, \
            watching out for quotes and escaping, then explain how to manually source it: {command}"
        clipea_execute_prompt(user_prompt)
    else:
        print(f"`alias` feature is only for zsh users. Current shell = {shell}")
