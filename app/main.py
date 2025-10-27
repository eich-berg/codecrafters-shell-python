import sys
import readline
import os

from .command import Command
from .cmd_map import cmd_map

last_completion_text = None
last_completion_matches = None

def tab_completer(text, state):
    """Tab completion function for builtin commands/external executables"""
    global last_completion_text, last_completion_matches

    # Get builtin commands that match
    builtin_options = [cmd for cmd in cmd_map.keys() if cmd.startswith(text)]
    # Get external executables that match
    exe_options = []
    path_dirs = os.getenv("PATH", "").split(os.pathsep)
    for path_dir in path_dirs:
        if os.path.isdir(path_dir):
            try:
                for item in os.listdir(path_dir):
                    if item.startswith(text) and os.access(os.path.join(path_dir, item), os.X_OK):
                        exe_options.append(item)
            except OSError:
                continue
    
    # Remove duplicates and combine
    all_options = sorted(set(builtin_options + exe_options))
    
    # Handle multiple matches
    if len(all_options) > 1:
        # First press: ring bell only
        if text != last_completion_text:
            sys.stdout.write('\a')
            sys.stdout.flush()
            last_completion_text = text
            last_completion_matches = all_options
            return None
        # Second press with same prefix: show completions
        else:
            sys.stdout.write('\n')  # New line
            sys.stdout.write("  ".join(all_options) + '\n')  # Two spaces between items + newline
            # Explicitly reprint the prompt and input
            sys.stdout.write(f"$ {text}")
            sys.stdout.flush()  # Force output to appear
            return None  # Don't complete, just show list
    
    # Single match
    last_completion_text = None
    last_completion_matches = None
    if state < len(all_options):
        return all_options[state] + " "
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