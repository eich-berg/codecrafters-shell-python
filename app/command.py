import sys

class Command:
    
    def __init__(self, args):
        self.command = args
        self.args = args.split()
    
    def cmd_parser(self):
        if self.args[0] == "exit":
            sys.exit(0)
        if self.args[0] == "echo":
            print(" ".join(arg for arg in self.args[1:]))
        print(f"{self.command}: command not found")
