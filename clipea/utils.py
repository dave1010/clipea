"""Utils
utils for the clipea application
"""
from typing import AnyStr
from pathlib import Path


def anystr_force_str(value: AnyStr) -> str:
    """Takes any AnyStr and gives back str

    Args:
        value (AnyStr)

    Returns:
        str: AnyStr's bytes decoded to str or it's str
    """
    return value.decode("utf-8") if isinstance(value, bytes) else value


def read_file(file_path: str) -> str:
    """Reads a file

    Args:
        file_path (str)

    Returns:
        str: file's content
    """
    with open(file_path, encoding="utf-8") as f:
        return anystr_force_str(f.read())


def get_config_file_with_fallback(
    home: str, fallback: str, appname: str, filename: str
) -> str:
    """Returns opinionated config file path

    Args:
        home (str): user's home
        fallback (str): fallback in case the file doesn't exist
        appname (str): your app name
        filename (str): file you're trying to get

    Returns:
        str: {home}/.config/{appname}/{filename} if it exists, else {fallback}/{filename}
    """
    config_path_obj: Path
    if (config_path_obj := Path(home + f"/.config/{appname}/{filename}")).is_file():
        return str(config_path_obj)
    return fallback + f"/{filename}"


def write_to_file(file_path: str, content: AnyStr, mode: str = "w") -> None:
    """Write to file

    Args:
        file_path (str)
        content (AnyStr)
        mode (str, optional): Defaults to "w".

    Returns:
        _type_: _description_
    """
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(content)
