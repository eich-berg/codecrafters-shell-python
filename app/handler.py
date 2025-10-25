import sys
import shutil
import subprocess
import os
from .cmd_map import cmd_map

class Handler:
    def __init__(self, args):
        self.args = args
    
    def handle_exit(self):
        sys.exit(0)
    
    def handle_echo(self):
        print(" ".join(arg for arg in self.args[1:]))
    
    def handle_type(self):
        if self.args[1] in cmd_map.keys():
            print(f"{self.args[1]} is a shell builtin")
        elif full_path := shutil.which(self.args[1]):
            print(f"{self.args[1]} is {full_path}")
        else:
            print(f"{self.args[1]}: not found")
    
    def handle_custom_exe(self):
        subprocess.run([self.args[0]] + self.args[1:])

    def handle_pwd(self):
        print(os.getcwd())