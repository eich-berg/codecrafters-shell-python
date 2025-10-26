import sys
import shutil
import subprocess
import os

# TDOO -> change some print statements to  sys.stderr.write

class Handler:
    def __init__(self, args):
        self.args = args
    
    def handle_exit(self):
        sys.exit(0)
    
    def handle_echo(self):
        print(" ".join(arg for arg in self.args[1:]))
    
    def handle_type(self):
        from .cmd_map import cmd_map
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
    
    def handle_cd(self):
        path = self.args[1]
        if path == "~":
            os.chdir(os.getenv("HOME"))
        elif os.path.exists(path):
            os.chdir(path)
        else:
            sys.stderr.write(f"cd: {path}: No such file or directory\n")