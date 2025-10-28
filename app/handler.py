import sys
import shutil
import os
import subprocess
import io
from .output import Output
from contextlib import redirect_stdout, redirect_stderr, redirect_stdin

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
            # --- Run left side (produce output) ---
            if left_cmd[0] in cmd_map:
                # Builtin: capture its stdout into memory
                buf = io.StringIO()
                left_handler = Handler(left_cmd)
                with redirect_stdout(buf):
                    cmd_map[left_cmd[0]](left_handler)
                left_output = buf.getvalue().encode()
            else:
                # External command
                p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                left_output, _ = p1.communicate()

            # --- Run right side (consume input) ---
            if right_cmd[0] in cmd_map:
                right_handler = Handler(right_cmd)

                # Case: builtin that *reads* stdin (not true for 'type', but future-proof)
                if getattr(cmd_map[right_cmd[0]], "reads_stdin", False):
                    with redirect_stdin(io.TextIOWrapper(io.BytesIO(left_output))):
                        cmd_map[right_cmd[0]](right_handler)
                else:
                    # Builtin ignores stdin (like 'type')
                    cmd_map[right_cmd[0]](right_handler)

            else:
                # External command: feed left_output into stdin
                p2 = subprocess.Popen(right_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                output, _ = p2.communicate(input=left_output)
                sys.stdout.write(output.decode())

        except Exception as e:
            print(f"Error executing pipeline: {e}", file=sys.stderr)
