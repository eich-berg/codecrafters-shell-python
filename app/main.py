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
#     readline.parse_and_bind("set enable-keypad on")

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

# Load history at startup
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

# Save history at exit
import atexit
atexit.register(readline.write_history_file, HISTORY_FILE)

def main():
    # Setup readline
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set enable-keypad on")

    history = []

    # Copy existing readline history to custom list
    for i in range(1, readline.get_current_history_length() + 1):
        history.append(readline.get_history_item(i))

    while True:
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue

        if not user_input:
            continue

        # Add to history immediately (even invalid commands)
        history.append(user_input)
        readline.add_history(user_input)

        # Execute command
        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()
