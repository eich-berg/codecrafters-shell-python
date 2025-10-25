import sys
import shutil
import subprocess
from .cmd_map import cmd_map
from .handler import Handler

class Command:
    
    def __init__(self, args):
        self.command = args
        self.args = args.split()
    
    def cmd_parser(self):

        handler = Handler(self.args)  # Pass args to handler

        if self.args[0] in cmd_map:
            cmd_map[self.args[0]](handler) # for ex. cmd_map["echo"](handler) -> calls Handler.handle_echo(handler)
            return
            
        # Handle external commands if not a builtin
        custom_exe = shutil.which(self.args[0]) # Find custom_exe in PATH
        if custom_exe:
            handler.handle_custom_exe()
            return
            
        print(f"{self.command}: command not found")