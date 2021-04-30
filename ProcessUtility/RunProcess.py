import subprocess


class RunProcess:

    def __init__(self):
        self.result = None

    def run(self, command):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        self.result = proc.stdout.read()
