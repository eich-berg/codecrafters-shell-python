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
import stat
from .command import Command

HISTORY_FILE = "/tmp/.shell_history"

def is_executable(file_path):
    try:
        st = os.stat(file_path)
        return stat.S_ISREG(st.st_mode) and (st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    except FileNotFoundError:
        return False

def get_matches(text):
    builtins = ["echo", "exit", "type", "pwd", "cd", "history"]
    results = []
    
    # Builtin matches
    for b in builtins:
        if b.startswith(text):
            results.append(b + " ")
    
    # External command matches
    path_env = os.environ.get("PATH", "")
    for path_dir in path_env.split(os.pathsep):
        if not os.path.isdir(path_dir):
            continue
        try:
            for name in os.listdir(path_dir):
                if name.startswith(text):
                    full_path = os.path.join(path_dir, name)
                    if is_executable(full_path):
                        results.append(name + " ")
        except (FileNotFoundError, PermissionError):
            continue
    
    return list(dict.fromkeys(results))

last_completion_text = None
tab_press_count = 0
cached_matches = []

def completer(text, state):
    global last_completion_text, tab_press_count, cached_matches
    
    if text != last_completion_text:
        last_completion_text = text
        tab_press_count = 0
        cached_matches = get_matches(text)
    
    if state == 0:
        tab_press_count += 1
    
    try:
        return cached_matches[state]
    except IndexError:
        return None

def display_matches_hook(substitution, matches, longest_match_length):
    global tab_press_count
    if len(matches) <= 1:
        tab_press_count = 0
        return
    if tab_press_count == 1:
        sys.stdout.write('\a')
        sys.stdout.flush()
    else:
        display_matches = [m.rstrip() for m in matches]
        print()
        print("  ".join(display_matches))
        print("$ " + readline.get_line_buffer(), end='', flush=True)

def main():
    # Set up readline properly
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    readline.set_completion_display_matches_hook(display_matches_hook)
    
    # Load existing history
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)

    while True:
        global tab_press_count, last_completion_text
        tab_press_count = 0
        last_completion_text = None
        
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        
        if not user_input:
            continue

        # Add to readline history
        readline.add_history(user_input)
        readline.write_history_file(HISTORY_FILE)
        
        # Get history from readline for the history command
        history = []
        for i in range(1, readline.get_current_history_length() + 1):
            history.append(readline.get_history_item(i))
        
        command = Command(user_input, history)
        command.cmd_parser()

if __name__ == "__main__":
    main()