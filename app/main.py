import sys
import readline
from .tab_completion import tab_completer
from .command import Command

def main():
    # Set up tab completion
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    # Enable history navigation (Up/Down arrows)
    readline.parse_and_bind("set enable-keypad on")

    history = []
    
    while True:
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        
        if not user_input:
            continue

        history.append(user_input)
        readline.add_history(user_input)
        readline.set_history_length(1000)
        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()
