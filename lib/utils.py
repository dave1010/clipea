from typing import AnyStr

def anystr_force_str(value: AnyStr) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    elif isinstance(value, str):
        return value
    raise ValueError("Unsupported type. Supported types: str, bytes")

def read_file(file_path:str) -> str:
    with open(file_path) as f:
        return anystr_force_str(f.read())