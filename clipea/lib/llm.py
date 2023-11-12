import llm
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
    buffer = ""

    for chunk in response:
        print(chunk, end="\n", flush=True)
        command += chunk
        if (new_line_pos := command.find("\n")) == -1:
            continue
        output_file = os.getenv("CLIPEA_CMD_OUTPUT_FILE")

        if command.startswith("$ "):
            print(command_prefix, end="")
            current_command = command[2:new_line_pos]
            command = command[new_line_pos + 1 :]
            if output_file:
                buffer += command
            else:
                cli.execute_with_prompt(current_command)
        else:
            command = ""

        if output_file:
            lib.utils.write_to_file(output_file, cmd)
