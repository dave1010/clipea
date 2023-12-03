"""Clipea application entry point
"""
import sys
import shutil
from clipea import router


def clipea_main() -> None:
    """
    Main function for the Clipea. It checks if the "llm" dependency is installed
    and then prompts the user for input. It then routes the user's input
    to the appropriate command in the router.
    """
    if shutil.which("llm") is None:
        sys.exit('Error: dependency "llm" not found. Run "clipea setup" to install')

    user_prompt = " ".join(sys.argv[1:])
    router.commands_router(user_prompt)


if __name__ == "__main__":
    clipea_main()
