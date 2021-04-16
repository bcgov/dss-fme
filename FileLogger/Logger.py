import os


class AppLogger:

    def __init__(self, name, clear=False):
        self.file_name = name
        if clear:
            if os.path.exists(name):
                os.remove(name)

    def write_line(self, obj):
        print("%s" % obj)
        f = open(self.file_name, "a")
        f.write("%s" % obj)
        f.write("\n")
        f.close()
