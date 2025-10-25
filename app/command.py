import sys

class Command:
    
    def __init__(self, arg):
        self.command = arg
    
    def cmd_parser(self):
        if self.command == "exit 0":
            sys.exit(0)
        print(f"{self.command}: command not found")