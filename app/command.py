import sys
import shutil
import subprocess

class Command:
    
    def __init__(self, args):
        self.command = args
        self.args = args.split()
    
    def cmd_parser(self):
        if self.args[0] == "exit":
            sys.exit(0)
        if self.args[0] == "echo":
            print(" ".join(arg for arg in self.args[1:]))
            return
        if self.args[0] == "type":
            if self.args[1] in ["exit", "echo", "type"]:
                print(f"{self.args[1]} is a shell builtin")
            elif full_path := shutil.which(self.args[1]):
                print(f"{self.args[1]} is {full_path}")
            else:
                print(f"{self.args[1]}: not found")
            return
        # Handle external commands - only if not a builtin
        custom_exe = shutil.which(self.args[0]) # Find custom_exe in PATH
        if custom_exe:
            # Execute it with arguments: custom_exe, arg1, arg2, argx, etc.
            subprocess.run([self.args[0]] + self.args[1:])
            return
        else:
            print(f"{self.command}: command not found")    