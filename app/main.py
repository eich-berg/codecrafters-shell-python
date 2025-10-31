import sys
import readline
import os
import atexit
from .tab_completion import tab_completer
from .command import Command


def main():
    readline.set_completer(tab_completer) # Set up tab completion
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set enable-keypad on") # Enable arrow key navigation
    readline.set_auto_history(False)

    histfile = os.getenv("HISTFILE", "/tmp/.shell_history")

    history = []
    # Copy histfile (prev. readline) history to custom history list 
    if os.path.exists(histfile):
        with open(histfile, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    readline.add_history(line)
                    history.append(line)

    # Register save function (append new history only)
    def append_history_on_exit():
        try:
            with open(histfile, "a") as f:
                # Only append commands entered after startup
                new_entries = history[len(history):]
                for cmd in new_entries:
                    f.write(cmd + "\n")
                f.write("\n")  # Add final empty line
        except Exception as e:
            print(f"Error appending to history: {e}", file=sys.stderr)

    atexit.register(append_history_on_exit)

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