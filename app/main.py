import sys
import readline
import os
from .command import Command
from .cmd_map import cmd_map

def tab_completer(text, state):
    """Tab completion function for builtin commands/external executables"""
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
    all_options = builtin_options + list(set(exe_options) - set(builtin_options))
    all_options.sort()
    
    # Handle multiple matches
    if len(all_options) > 1:
        if state == 0:
            # First TAB press with multiple matches - ring bell
            sys.stdout.write('\a')  # Bell character
            sys.stdout.flush()
            return None  # Don't complete anything
        elif state == 1:
            # Second TAB press - show all options
            print()  # New line
            print("  ".join(all_options))  # Two spaces between items
            return None  # Don't complete, just show list
    
    # Normal single-match completion
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
