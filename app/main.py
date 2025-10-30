import sys
import readline
import os
from .tab_completion import tab_completer
from .command import Command


def main():
    # Set up tab completion
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    # Enable arrow key navigation
    readline.parse_and_bind("set enable-keypad on")
    readline.set_auto_history(False)

    history = []

    # Copy existing readline history to your custom list
    for i in range(readline.get_current_history_length()):
        history.append(readline.get_history_item(i + 1))
    
    while True:
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        
        if not user_input:
            continue

        history.append(user_input)
        readline.add_history(user_input)
        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()
