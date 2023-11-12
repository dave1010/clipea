import sys
import clipea
import shutil

if __name__ == "__main__":
    if shutil.which("llm") == None:
        exit('Error: dependency "llm" not found. Run "clipea setup" to install')

    user_prompt = " ".join(sys.argv[1:])
    clipea.commands_router(user_prompt)
