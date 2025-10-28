import sys
import readline
from .tab_completion import tab_completer
from .command import Command

def main():
    # Set up tab completion
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input().strip()
        except EOFError:
            break

        if user_input:
            command = Command(user_input)
            command.cmd_parser()

if __name__ == "__main__":
    main()