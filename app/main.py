import sys

def main():
    sys.stdout.write("$ ")
    parse_input()
    main()

def parse_input():
    # Captures the user's command in the "command" variable
    command = input()
    print(f"{command}: command not found")


if __name__ == "__main__":
    main()
