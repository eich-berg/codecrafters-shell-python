# import shutil
# import shlex
# from .cmd_map import cmd_map
# from .handler import Handler
    
# class Command:

#     def __init__(self, args, history=None):
#         self.command = args
#         self.args = shlex.split(args)  # This handles single quotes automatically
#         self.history = history or []
    
#     def cmd_parser(self):
#         # Check for pipe operator
#         if "|" in self.args:
#             # Split into multiple commands by '|'
#             commands = []
#             current = []
#             for arg in self.args:
#                 if arg == "|":
#                     if current:
#                         commands.append(current)
#                         current = []
#                 else:
#                     current.append(arg)
#             if current:
#                 commands.append(current)

#             # Pass the list of commands to handler
#             handler = Handler(self.args, history=self.history)
#             handler.handle_pipeline(commands)
#             return
        
#         redirect_type = None
#         filename = None
#         command_args = self.args

#         # Check for redirect types
#         for op in [">", "1>", "2>", ">>", "1>>", "2>>"]:
#             if op in self.args:
#                 # Find the operator and filename
#                 op_index = self.args.index(op)
#                 filename = self.args[op_index + 1]
#                 command_args = self.args[:op_index] # Remove redirect parts
#                 redirect_type = op
#                 break

#         handler = Handler(command_args, redirect_type, filename, self.history)

        
#         if command_args[0] in cmd_map:
#             cmd_map[command_args[0]](handler) # ex. cmd_map["echo"](handler) calls Handler.handle_echo(handler)
#             return
                
#         # Handle external commands if not a builtin
#         custom_exe = shutil.which(self.args[0]) # Find custom_exe in PATH
#         if custom_exe:
#             handler.handle_custom_exe()
#             return
            
#         print(f"{self.command}: command not found")

import shlex
import shutil
from .handler import Handler
from .cmd_map import cmd_map

class Command:
    def __init__(self, args, history=None):
        self.command = args
        self.args = shlex.split(args)
        self.history = history or []

    def cmd_parser(self):
        # Handle pipelines
        if "|" in self.args:
            commands = []
            current = []
            for arg in self.args:
                if arg == "|":
                    if current:
                        commands.append(current)
                        current = []
                else:
                    current.append(arg)
            if current:
                commands.append(current)
            handler = Handler(self.args, history=self.history)
            handler.handle_pipeline(commands)
            return

        # Handle redirections
        redirect_type = None
        filename = None
        command_args = self.args
        for op in [">", "1>", "2>", ">>", "1>>", "2>>"]:
            if op in self.args:
                op_index = self.args.index(op)
                filename = self.args[op_index + 1]
                command_args = self.args[:op_index]
                redirect_type = op
                break

        handler = Handler(command_args, redirect_type, filename, self.history)

        # Builtins
        if command_args[0] in cmd_map:
            cmd_map[command_args[0]](handler)
            return

        # External commands
        if shutil.which(command_args[0]):
            handler.handle_custom_exe()
            return

        print(f"{self.command}: command not found")
