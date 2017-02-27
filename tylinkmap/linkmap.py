SESSION_PREFIX_PATH = '# Path: '


class LinkMap(object):
    def __init__(self):
        self.path = ''
        self.arch = ''

    def paring(self, filename):
        with open(filename, 'r') as f:
            line = f.readline()
            if line.startswith(SESSION_PREFIX_PATH):
                self.path = line[len(SESSION_PREFIX_PATH):]