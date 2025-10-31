import sys
import shutil
import os
import subprocess
import readline
import io
from .output import Output
from contextlib import redirect_stdout

class Handler:

    def __init__(self, args, redirect_type=None, filename=None, history=None):
        self.args = args
        self.output_handler = Output(redirect_type, filename)
        self.history = history or []

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

    def handle_history(self):
        # Handle history -r <file> command
        error_msg = "history: -r/-w/-a: options require an argument"
        if len(self.args) > 1 and self.args[1] == "-r":
            if len(self.args) > 2:
                history_file = self.args[2]
                self._read_history_from_file(history_file)
            else:
                self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)
            return
        elif len(self.args) > 1 and self.args[1] == "-w":
            if len(self.args) > 2:
                history_file = self.args[2]
                self._write_history_to_file(history_file)
            else:
                self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)
            return
        elif len(self.args) > 1 and self.args[1] == "-a":
            if len(self.args) > 2:
                history_file = self.args[2]
                self._append_history_to_file(history_file)
            else:
                self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)
            return
    
        n = int(self.args[1]) if len(self.args) > 1 and self.args[1].isdigit() else None
        entries = self.history[-n:] if n else self.history
        start = len(self.history) - len(entries) + 1
        output = "\n".join(f"    {i}  {cmd}" for i, cmd in enumerate(entries, start))
        self.output_handler.execute_builtin_with_redirect(output, is_error=False)


    def _read_history_from_file(self, history_file):
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:  # Skip empty lines
                            self.history.append(line)
                            # Also add to readline history for tab completion
                            readline.add_history(line)
        except Exception as e:
            error_msg = f"history: cannot read history file: {e}"
            self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)
            
    def _write_history_to_file(self, history_file):
        try:
            with open(history_file, 'w') as f:
                for command in self.history:
                    f.write(command + '\n')
        except Exception as e:
            error_msg = f"history: cannot write history file: {e}"
            self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)

    def _append_history_to_file(self, history_file):
        try:
            with open(history_file, 'a') as f:
                for command in self.history:
                    f.write(command + '\n')
            self.history.clear()
        except Exception as e:
            error_msg = f"history: cannot append to history file: {e}"
            self.output_handler.execute_builtin_with_redirect(error_msg, is_error=True)

    def handle_pipeline(self, commands):
        from .cmd_map import cmd_map

        processes = []
        prev_stdout = None
        builtin_output = None

        try:
            for i, cmd in enumerate(commands):
                is_builtin = cmd[0] in cmd_map
                is_last = (i == len(commands) - 1)

                # Case 1: Builtin command
                if is_builtin:
                    buf = io.StringIO()
                    h = Handler(cmd)
                    with redirect_stdout(buf):
                        cmd_map[cmd[0]](h)
                    builtin_output = buf.getvalue().encode()
                    prev_stdout = io.BytesIO(builtin_output)
                    continue

                # Case 2: External command
                stdin = None
                if builtin_output is not None:
                    stdin = subprocess.PIPE
                elif prev_stdout is not None:
                    stdin = prev_stdout

                stdout = subprocess.PIPE if not is_last else None

                p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout)

                if builtin_output is not None:
                    p.communicate(input=builtin_output)
                    builtin_output = None
                    prev_stdout = p.stdout if not is_last else None
                else:
                    prev_stdout = p.stdout

                processes.append(p)

            # Handle last command being a builtin
            if commands and commands[-1][0] in cmd_map and len(commands) > 1:
                last_cmd = commands[-1]
                last_is_builtin = last_cmd[0] in cmd_map
                if last_is_builtin:
                    # Read the output of the previous (external) pipeline
                    if prev_stdout:
                        prev_output, _ = processes[-1].communicate()
                        prev_stdout = None
                    else:
                        prev_output = b""

                    buf_in = io.StringIO(prev_output.decode())
                    sys.stdin = buf_in  # Temporarily redirect stdin
                    try:
                        h = Handler(last_cmd)
                        cmd_map[last_cmd[0]](h)
                    finally:
                        sys.stdin = sys.__stdin__
                    return

            # Default final output case
            if processes:
                last_proc = processes[-1]
                output, _ = last_proc.communicate()
                if output:
                    sys.stdout.write(output.decode())
                for p in processes[:-1]:
                    p.wait()

            elif builtin_output is not None:
                sys.stdout.write(builtin_output.decode())

        except Exception as e:
            print(f"Error executing pipeline: {e}", file=sys.stderr)
        finally:
            for p in processes:
                try:
                    p.terminate()
                except Exception:
                    pass