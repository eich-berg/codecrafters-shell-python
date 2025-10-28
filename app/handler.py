import sys
import shutil
import os
import subprocess
import io
from .output import Output
from contextlib import redirect_stdout, redirect_stderr

def redirect_stdin(target):
    old_stdin = sys.stdin
    try:
        sys.stdin = target
        yield
    finally:
        sys.stdin = old_stdin

class Handler:
    def __init__(self, args, redirect_type=None, filename=None):
        self.args = args
        self.output_handler = Output(redirect_type, filename)
        
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


    def handle_pipeline(self, left_cmd, right_cmd):
        from .cmd_map import cmd_map
        try:
            # --- Case 1: both are external (streaming) ---
            if left_cmd[0] not in cmd_map and right_cmd[0] not in cmd_map:
                p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE)
                p2 = subprocess.Popen(right_cmd, stdin=p1.stdout)
                p1.stdout.close()  # Allow p1 to receive SIGPIPE if p2 exits early
                p2.wait()          # Wait for second command (e.g., `head`) to finish
                p1.terminate()     # Stop `tail -f` or other continuous producer
                return

            # --- Case 2: left is builtin, right is external ---
            if left_cmd[0] in cmd_map and right_cmd[0] not in cmd_map:
                buf = io.StringIO()
                left_handler = Handler(left_cmd)
                with redirect_stdout(buf):
                    cmd_map[left_cmd[0]](left_handler)
                left_output = buf.getvalue().encode()

                p2 = subprocess.Popen(right_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                output, _ = p2.communicate(input=left_output)
                sys.stdout.write(output.decode())
                return

            # --- Case 3: left is external, right is builtin ---
            if left_cmd[0] not in cmd_map and right_cmd[0] in cmd_map:
                p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE)
                left_output, _ = p1.communicate()
                right_handler = Handler(right_cmd)
                cmd_map[right_cmd[0]](right_handler)
                return

            # --- Case 4: both are builtins ---
            if left_cmd[0] in cmd_map and right_cmd[0] in cmd_map:
                buf = io.StringIO()
                left_handler = Handler(left_cmd)
                with redirect_stdout(buf):
                    cmd_map[left_cmd[0]](left_handler)
                left_output = buf.getvalue().encode()
                right_handler = Handler(right_cmd)
                cmd_map[right_cmd[0]](right_handler)
                return

        except Exception as e:
            print(f"Error executing pipeline: {e}", file=sys.stderr)
