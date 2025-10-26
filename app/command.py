import shutil
import shlex
from .cmd_map import cmd_map
from .handler import Handler

class Command:
    
    def __init__(self, args):
        self.command = args
        self.args = shlex.split(args)  # This handles single quotes automatically
    
    def cmd_parser(self):

        redirect = False
        filename = None
        command_args = self.args

        # Check for > or 1> in args
        if ">" in self.args or "1>" in self.args:
            # Find the operator and filename
            op_index = self.args.index(">") if ">" in self.args else self.args.index("1>")
            filename = self.args[op_index + 1]
            command_args = self.args[:op_index] # Remove redirect parts
            redirect = True

        handler = Handler(command_args, redirect, filename)
        
        if command_args[0] in cmd_map:
            cmd_map[command_args[0]](handler) # ex. cmd_map["echo"](handler) calls Handler.handle_echo(handler)
            return
                
        # Handle external commands if not a builtin
        custom_exe = shutil.which(self.args[0]) # Find custom_exe in PATH
        if custom_exe:
            handler.handle_custom_exe()
            return
            
        print(f"{self.command}: command not found")