import sys
import readline
import os
from .tab_completion import tab_completer
from .command import Command


def main():
    readline.set_completer(tab_completer) # Set up tab completion
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set enable-keypad on") # Enable arrow key navigation
    readline.set_auto_history(False)

    histfile = os.getenv("HISTFILE", "/tmp/.shell_history")

    history = []
    # Copy existing readline history to custom history list 
    # for i in range(readline.get_current_history_length()):
    #     history.append(readline.get_history_item(i + 1))
    if os.path.exists(histfile):
        with open(histfile, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                readline.add_history(line)
                history.append(line)
    
    while True:
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        
        if not user_input:
            continue

        history.append(user_input)
        readline.add_history(user_input)

        # Save history back to file
        with open(histfile, "w") as f:
            for cmd in history:
                f.write(cmd + "\n")

        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()