import llm
import lib.cli
import llm.cli
import os


def init_llm(llm_model: str = "") -> llm.Model:
    try:
        model = llm.get_model(
            llm_model or llm.cli.get_default_model(filename="clipea_default_model.txt")
        )
    except llm.UnknownModelError:
        exit(f"Error, unknown model: {model.model_id}")

    if model.needs_key:
        model.key = llm.get_key("", model.needs_key, model.key_env_var)
    return model


def stream_commands(response: llm.Response, command_prefix: str = "") -> None:
    command: str = ""
    output_file: str = os.getenv("CLIPEA_CMD_OUTPUT_FILE")
    buffer: str = ""
    current_command: str = ""

    def process_command():
        nonlocal current_command, buffer, output_file, command

        current_command = command[2:new_line_pos]
        command = command[new_line_pos + 1 :]

        if output_file != None:
            buffer += current_command + os.linesep
        else:
            lib.cli.execute_with_prompt(current_command)

    print(command_prefix, end="")
    for chunk in response:
        print(chunk, end="", flush=True)
        command += chunk

        if (new_line_pos := command.find(os.linesep)) == -1:
            continue
        if command.startswith("$ "):
            process_command()
        else:
            print(command_prefix, end=" ")
            command = ""

    # llm CLI put a line feed manually to it's response, but not it's library
    # We have to do this to manage the case where the model returns a 
    # non-linefeed terminated string.
    # It also explains why there is a capturing nested function `process_command`
    if command != "":
        print()
        process_command()

    if output_file:
        lib.utils.write_to_file(
            output_file.replace(os.linesep, f";\ {os.linesep}", -1), cmd
        )
