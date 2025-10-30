# import sys
# import readline
# import os
# from .tab_completion import tab_completer
# from .command import Command

# HISTORY_FILE = "/tmp/.shell_history"

# def main():
#     # Set up tab completion
#     readline.set_completer(tab_completer)
#     readline.parse_and_bind("tab: complete")
#     # Enable arrow key navigation
#     # readline.parse_and_bind("set enable-keypad on")

#     # Load existing history (if any)
#     if os.path.exists(HISTORY_FILE):
#         readline.read_history_file(HISTORY_FILE)

#     history = []


#     # Copy existing readline history to your custom list
#     for i in range(readline.get_current_history_length()):
#         history.append(readline.get_history_item(i + 1))
    
#     while True:
#         try:
#             user_input = input("$ ").strip()
#         except EOFError:
#             break
        
#         if not user_input:
#             continue

#         history.append(user_input)
#         readline.add_history(user_input)
#         readline.write_history_file(HISTORY_FILE)
#         command = Command(user_input, history)
#         command.cmd_parser()

# if __name__ == "__main__":
#     main()

import sys
import readline
import os
from .tab_completion import tab_completer
from .command import Command

HISTORY_FILE = "/tmp/.shell_history"

# Load previous history
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

# Save history on exit
import atexit
atexit.register(readline.write_history_file, HISTORY_FILE)

def main():
    # Set up tab completion
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set enable-keypad on")  # Up/Down arrows

    history = []

    while True:
        try:
            # readline handles up-arrow
            user_input = input("$ ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue

        if not user_input:
            continue

        # Add to readline history for up-arrow
        readline.add_history(user_input)
        # Add to your own history for Command
        history.append(user_input)

        # Parse and execute
        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()
