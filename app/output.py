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

    def execute_builtin_with_redirect(self, text, is_error=False):
        if self.redirect_type in [">", "1>"]:
            with open(self.filename, "w") as f:
                f.write(text + "\n")
        elif self.redirect_type in [">>", "1>>"]:
            with open(self.filename, "a") as f:
                f.write(text + "\n")
        else:
            self._output(text, is_error)

    def execute_external_with_redirect(self, args):
        if self.redirect_type in [">", "1>"]:
            with open(self.filename, "w") as f:
                subprocess.run(args, stdout=f)
        elif self.redirect_type in [">>", "1>>"]:
            with open(self.filename, "a") as f:
                subprocess.run(args, stdout=f)
        else:
            subprocess.run(args)
