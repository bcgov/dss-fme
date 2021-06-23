import os


class AppLogger:

    def __init__(self, name, save_file=True, clear=False):
        self.file_name = name
        self.save_file = save_file
        if self.save_file and clear:
            if os.path.exists(name):
                os.remove(name)

    def write_line(self, obj):
        # text = None
        # if isinstance(obj, object):
        #     text = json.dumps(obj)
        # else:
        #     text = obj
        print("%s" % obj)
        if self.save_file:
            out_dir = os.path.dirname(self.file_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            f = open(self.file_name, "a")
            f.write("%s" % obj)
            f.write("\n")
            f.close()
