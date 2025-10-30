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

def main():
    # Tab completion + arrow keys
    readline.set_completer(tab_completer)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set enable-keypad on")

    # Ensure history file exists (optional)
    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "a").close()

    try:
        while True:
            # ---- critical: reload history fresh before each prompt ----
            try:
                readline.clear_history()
            except Exception:
                # older readline may not have clear_history()
                pass

            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception:
                # ignore read errors; file was ensured above
                pass
            # ----------------------------------------------------------

            try:
                user_input = input("$ ").strip()
            except EOFError:
                break

            if not user_input:
                continue

            # Add new entry and persist
            readline.add_history(user_input)
            try:
                readline.write_history_file(HISTORY_FILE)
            except Exception:
                pass

            # Execute command
            Command(user_input).cmd_parser()

    except KeyboardInterrupt:
        print()
