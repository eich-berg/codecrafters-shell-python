import sys
import shutil
import subprocess
import os

# TDOO -> change some print statements to  sys.stderr.write

class Handler:
    def __init__(self, args, redirect_type=None, filename=None):
        self.args = args
        self.redirect_type = redirect_type
        self.filename = filename
        
    def handle_exit(self):
        sys.exit(0)
    
    def handle_echo(self):
        output = " ".join(arg for arg in self.args[1:])
        if self.redirect_type == "2>":
            open(self.filename, 'w').close()  # Create empty file for stderr redirect
            print(output) # Print output to terminal
        elif self.redirect_type in [">", "1>"]:  # Only redirect stdout
            with open(self.filename, 'w') as f:
                f.write(output + "\n")
        else:
            print(output)
    
    def handle_type(self):
        from .cmd_map import cmd_map
        if self.args[1] in cmd_map.keys():
            print(f"{self.args[1]} is a shell builtin")
        elif full_path := shutil.which(self.args[1]):
            print(f"{self.args[1]} is {full_path}")
        else:
            print(f"{self.args[1]}: not found")
        
    def handle_custom_exe(self):
        if self.redirect_type:
            with open(self.filename, 'w') as f:
                if self.redirect_type == "2>":
                    subprocess.run([self.args[0]] + self.args[1:], stderr=f)
                else:  # ">" or "1>"
                    subprocess.run([self.args[0]] + self.args[1:], stdout=f)
        else:
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