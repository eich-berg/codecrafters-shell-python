import shutil
import sys
import shlex
import subprocess
from .cmd_map import cmd_map
from .handler import Handler

class Command:
    
    def __init__(self, args):
        self.command = args
        self.args = shlex.split(args)  # This handles single quotes automatically
    
    def cmd_parser(self):

        # Check for pipe operator
        if "|" in self.args:
            pipe_index = self.args.index("|")
            left_command = self.args[:pipe_index]
            right_command = self.args[pipe_index + 1:]
            
            # Handle pipeline
            handler = Handler(self.args)
            handler.handle_pipeline(left_command, right_command)
            return
        
        redirect_type = None
        filename = None
        command_args = self.args

        # Check for redirect types
        for op in [">", "1>", "2>", ">>", "1>>", "2>>"]:
            if op in self.args:
                # Find the operator and filename
                op_index = self.args.index(op)
                filename = self.args[op_index + 1]
                command_args = self.args[:op_index] # Remove redirect parts
                redirect_type = op
                break

        handler = Handler(command_args, redirect_type, filename)
        
        if command_args[0] in cmd_map:
            cmd_map[command_args[0]](handler) # ex. cmd_map["echo"](handler) calls Handler.handle_echo(handler)
            return
                
        # Handle external commands if not a builtin
        custom_exe = shutil.which(self.args[0]) # Find custom_exe in PATH
        if custom_exe:
            handler.handle_custom_exe()
            return
            
        print(f"{self.command}: command not found")


    def handle_pipeline(self, left_cmd, right_cmd):
        try:
            p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(right_cmd, stdin=p1.stdout)
            
            p1.stdout.close()
            p2.wait()  # Wait for second command to finish
            p1.terminate()  # Stop the first command when second finishes
            
        except Exception as e:
            print(f"Error executing pipeline: {e}", file=sys.stderr)