import sys
import shutil
import os
from .output import Output

class Handler:
    def __init__(self, args, redirect_type=None, filename=None):
        self.args = args
        self.output_handler = Output(redirect_type, filename)
        
    def handle_exit(self):
        sys.exit(0)
    
    def handle_echo(self):
        output = " ".join(arg for arg in self.args[1:])
        self.output_handler.execute_builtin_with_redirect(output, is_error=False)
    
    def handle_type(self):
        from .cmd_map import cmd_map
        if self.args[1] in cmd_map.keys():
            output = f"{self.args[1]} is a shell builtin"
            self.output_handler.execute_builtin_with_redirect(output, is_error=False)
        elif full_path := shutil.which(self.args[1]):
            output = f"{self.args[1]} is {full_path}"
            self.output_handler.execute_builtin_with_redirect(output, is_error=False)
        else:
            output = f"{self.args[1]}: not found"
            self.output_handler.execute_builtin_with_redirect(output, is_error=True)
    
    def handle_custom_exe(self):
        self.output_handler.execute_external_with_redirect([self.args[0]] + self.args[1:])

    def handle_pwd(self):
        output = os.getcwd()
        self.output_handler.execute_builtin_with_redirect(output, is_error=False)
    
    def handle_cd(self):
        path = self.args[1]
        if path == "~":
            os.chdir(os.getenv("HOME"))
        elif os.path.exists(path):
            os.chdir(path)
        else:
            error_msg = f"cd: {path}: No such file or directory"
            self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)