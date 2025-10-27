import sys
import subprocess

class Output:
    def __init__(self, redirect_type=None, filename=None):
        self.redirect_type = redirect_type
        self.filename = filename
    
    def _output(self, text, is_error=False):
        if is_error:
            sys.stderr.write(text + "\n")
            sys.stderr.flush()
        else:
            print(text)
    
    def _handle_stdout_redirect(self, output):
        if self.redirect_type in [">>", "1>>"]:
            with open(self.filename, 'a') as f:
                f.write(output + "\n")
        else:  # ">" or "1>"
            with open(self.filename, 'w') as f:
                f.write(output + "\n")
    
    def _handle_stderr_redirect(self):
        if self.redirect_type == "2>>":
            open(self.filename, 'a').close()
        else:  # "2>"
            open(self.filename, 'w').close()
    
    def execute_builtin_with_redirect(self, output_text, is_error=False):
        if self.redirect_type in [">", "1>", ">>", "1>>"] and not is_error:
            self._handle_stdout_redirect(output_text)
        elif self.redirect_type in ["2>", "2>>"] and is_error:
            self._handle_stderr_redirect()
            self._output(output_text, is_error)
        elif self.redirect_type in ["2>", "2>>"] and not is_error:
            self._handle_stderr_redirect()
            self._output(output_text, is_error)
        else:
            self._output(output_text, is_error)
    
    def execute_external_with_redirect(self, command_args):
        if self.redirect_type in [">>", "1>>"]:
            with open(self.filename, 'a') as f:
                subprocess.run(command_args, stdout=f)
        elif self.redirect_type in [">", "1>"]:
            with open(self.filename, 'w') as f:
                subprocess.run(command_args, stdout=f)
        elif self.redirect_type == "2>":
            with open(self.filename, 'w') as f:
                subprocess.run(command_args, stderr=f)
        elif self.redirect_type == "2>>":
            with open(self.filename, 'a') as f:
                subprocess.run(command_args, stderr=f)
        else:
            subprocess.run(command_args)