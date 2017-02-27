PREFIX_PATH = '# Path: '
PREFIX_ARCH = '# Arch: '


class LinkMap(object):
    def __init__(self):
        self.path = ''
        self.arch = ''

    def paring(self, filename):
        with open(filename, 'r') as f:
            line = f.readline()
            if line.startswith(PREFIX_PATH):
                self.path = line[len(PREFIX_PATH):]
            elif line.startswith(PREFIX_ARCH):
                self.arch = line[len(PREFIX_ARCH):]