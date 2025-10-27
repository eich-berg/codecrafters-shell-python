import sys
import readline
from .command import Command
from .cmd_map import cmd_map
import argparse

def tab_completer(text, state):
    """Tab completion function for builtin commands"""
    options = [cmd for cmd in cmd_map.keys() if cmd.startswith(text)]
    if state < len(options):
        return options[state] + " "  # Note the space at the end
    return None

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