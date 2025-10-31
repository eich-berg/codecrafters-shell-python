import sys
import readline
import os
from .cmd_map import cmd_map

last_completion_text = None

def longest_common_prefix(strings):
    if not strings:
        return ""
    prefix = strings[0]
    for s in strings[1:]:
        i = 0
        while i < len(prefix) and i < len(s) and prefix[i] == s[i]:
            i += 1
        prefix = prefix[:i]
    return prefix

def tab_completer(text, state):
    global last_completion_text

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

    # No matches
    if not all_options:
        return None

    # Single match: complete fully
    if len(all_options) == 1:
        if state == 0:
            return all_options[0] + " "
        return None

    # Multiple matches: try longest common prefix
    lcp = longest_common_prefix(all_options)
    if len(lcp) > len(text):
        if state == 0:
            return lcp
        return None
    
    # First press: ring bell only
    if text != last_completion_text:
        sys.stdout.write('\a')
        sys.stdout.flush()
        last_completion_text = text
        # last_completion_matches = all_options
        return None
    # Second press with same prefix: show completions
    else:
        sys.stdout.write('\n')  # New line
        sys.stdout.write("  ".join(all_options) + '\n')  # Two spaces between items + newline
        # Explicitly reprint the prompt and input
        sys.stdout.write(f"$ {text}")
        sys.stdout.flush()  # Force output to appear
        return None  # Don't complete, just show list
