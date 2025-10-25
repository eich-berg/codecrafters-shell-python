import sys
from command import Command
import argparse

def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input().strip()
        except EOFError:
            break

        if user_input:
            command = Command(user_input)
            command.cmd_parser()

if __name__ == "__main__":
    main()