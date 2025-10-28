import sys
import shutil
import os
import subprocess
import io
from contextlib import redirect_stdout, redirect_stdin
from .output import Output
from .cmd_map import cmd_map

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
        try:
        #     p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE)
        #     p2 = subprocess.Popen(right_cmd, stdin=p1.stdout)
            
        #     p1.stdout.close()
        #     p2.wait()  # Wait for second command to finish
        #     p1.terminate()  # Stop the first command when second finishes
            
        # except Exception as e:
        #     print(f"Error executing pipeline: {e}", file=sys.stderr)

            # Check if left command is a builtin
            if left_cmd[0] in cmd_map:
                # For builtin commands, we need to capture their output manually
                output_buffer = io.StringIO()
                left_handler = Handler(left_cmd)
                
                with redirect_stdout(output_buffer):
                    cmd_map[left_cmd[0]](left_handler)
                
                left_output = output_buffer.getvalue().encode()
            else:
                # External command - use subprocess
                p1 = subprocess.Popen(left_cmd, stdout=subprocess.PIPE)
                left_output = p1.communicate()[0]
                if p1.returncode != 0:
                    # Handle command failure if needed
                    pass
            
            # Check if right command is a builtin  
            if right_cmd[0] in cmd_map:
                # For builtin commands that read from stdin in pipeline
                # Create a temporary file-like object with the left command's output
                input_buffer = io.BytesIO(left_output)
                right_handler = Handler(right_cmd)
                # For builtins that might read from stdin 
                # For now, just execute normally since type/echo don't read stdin
                with redirect_stdin(io.TextIOWrapper(input_buffer)):
                    cmd_map[right_cmd[0]](right_handler)
            else:
                # External command - pipe the output
                p2 = subprocess.Popen(right_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                output = p2.communicate(input=left_output)[0]
                print(output.decode(), end='')
                
        except Exception as e:
            print(f"Error executing pipeline: {e}")