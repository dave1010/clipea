"""Clipea application entry point
"""
import sys
import shutil
from clipea import router


def clipea_main() -> None:
    if shutil.which("llm") is None:
        sys.exit('Error: dependency "llm" not found. Run "clipea setup" to install')

    USER_PROMPT = " ".join(sys.argv[1:])
    router.commands_router(USER_PROMPT)


if __name__ == "__main__":
    clipea_main()
