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
        if self.args[0] == "type":
            if self.args[1] in ["exit", "echo", "type"]:
                print(f"{self.args[1]} is a shell builtin")
            else:
                print(f"{self.args[1]}: not found")
        else:
            print(f"{self.command}: command not found")