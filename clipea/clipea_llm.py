"""LLM
Interactions with `llm` python library
"""

import os
import sys
import llm.cli
import llm
import clipea.cli
from clipea import ENV, HOME_PATH, CLIPEA_DIR, utils
from loguru import logger as log


def init_llm(llm_model: str = "") -> llm.Model:
    """Initialize base llm library with user's `llm_model`

    Args:
        llm_model (str, optional): LLM model name (ex: "gpt-4").
                                   Defaults to content of {clipea config}/clipea_default_model.txt.

    Returns:
        llm.Model
    """
    clipea_default_model_path = utils.get_config_file_with_fallback(
        home=HOME_PATH,
        fallback=CLIPEA_DIR,
        appname="clipea",
        filename="clipea_default_model.txt",
    )
    model = llm.get_model(
        llm_model or llm.cli.get_default_model(filename=clipea_default_model_path)
    )

    if model.needs_key:
        model.key = llm.get_key("", model.needs_key, model.key_env_var)
    return model


def stream_commands(response: llm.Response, command_prefix: str = "") -> None:
    """Streams llm response which returns shell commands
    If a valid shell commands is returned, either prompt to execute it or
    put it in zsh's command buffer
    The processing is done internally with a nested function `process_command`
    A command is considered valid if it starts with '$ ' and is a full line of answer

    Args:
        response (llm.Response): LLM's answer to user's prompt
        command_prefix (str, optional): What to write before streaming the commands. Defaults to "".
    """
    command: str = ""
    output_file: str | None = os.getenv("CLIPEA_CMD_OUTPUT_FILE")
    approved_cmd_list: str = ""
    new_line_pos: int

    def process_command():
        nonlocal command, approved_cmd_list, new_line_pos

        cmd_unapproved: str
        if new_line_pos > 0:
            cmd_unapproved = command[2:new_line_pos]
        else:
            cmd_unapproved = command[2:]
        command = command[new_line_pos + 1 :]

        # if in an interactive shell, prompt the user
        # for changes then run the command once approved.
        cmd_executed = None
        if sys.stdin.isatty():
            cmd_executed = clipea.cli.execute_after_approval(
                cmd_unapproved, shell=ENV["shell"]
            )
        if output_file is not None:
            cmd_to_add: str # command to add to the output file
            if sys.stdin.isatty():
                if not cmd_executed:
                    return  # no command was approved and executed
                cmd_to_add = cmd_executed
            cmd_to_add = cmd_unapproved
            log.debug("Adding to command list: ", cmd_to_add)
            approved_cmd_list += cmd_to_add + os.linesep

    print(command_prefix, end="")
    for chunk in response:
        print(chunk, end="", flush=True)
        command += chunk

        if (new_line_pos := command.find(os.linesep)) == -1:
            continue
        if command.startswith("$ "):
            process_command()
        else:
            command = ""

    # llm CLI put a line feed manually to it's response, but not it's library
    # We have to do this to manage the case where the model returns a
    # non-linefeed terminated string.
    # It also explains why there is a capturing nested function `process_command`
    if command.startswith("$ "):
        print()
        process_command()

    if output_file:
        cmd_lines = approved_cmd_list.rstrip(os.linesep).split(os.linesep)
        cmd_lines = [cmd for cmd in cmd_lines if cmd] # remove empty lines
        log.debug(f"Writing {len(cmd_lines)} lines to {output_file}")
        utils.write_to_file(
            output_file,
            ";".join(
                cmd_lines,
            ) + os.linesep,
        )
