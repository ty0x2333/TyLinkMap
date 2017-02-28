import re
import os
BLOCK_PATH = 'Path'
BLOCK_ARCH = 'Arch'
BLOCK_OBJECT_FILES = 'Object files'
BLOCK_SESSION = 'Sections'
BLOCK_SYMBOLS = 'Symbols'
BLOCK_DEAD_STRIPPED_SYMBOLS = 'Dead Stripped Symbols'


class FileObject(object):
    def __init__(self, module, number=0, filename=''):
        self.number = number
        self.filename = filename
        self.module = module

    def __str__(self):
        return "[%d] %s %s" % (self.number, self.filename, self.module)


class Section(object):
    def __init__(self, address, size, segment, section):
        self.address = address
        self.size = size
        self.segment = segment
        self.section = section

    def __str__(self):
        return "%s %s %s %s" % (self.address, self.size, self.segment, self.section)


class Symbol(object):
    def __init__(self, address, size, file_number, name):
        self.address = address
        self.size = size
        self.file_number = file_number
        self.name = name

    def __str__(self):
        return "%s %s [%d] %s" % (self.address, self.size, self.file_number, self.name)


class LinkMap(object):
    def __init__(self):
        self.path = ''
        self.arch = ''
        self.last_block = ''
        self.file_objs = []
        self.sections = []
        self.symbols = []

    @property
    def target_name(self):
        return os.path.basename(self.path)

    def paring(self, filename):
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                if self.__paring_block(line):
                    continue

                if self.last_block == BLOCK_OBJECT_FILES:
                    compiler = re.compile(r"\[\s*(?P<num>\d*)\]\s*(?P<content>.*)")
                    content_compiler = re.compile(r"(?P<path>.*)\((?P<filename>.*)\)")
                    match = compiler.match(line)
                    if not match:
                        # print 'Warning: can not match object file!'
                        continue

                    num = int(match.group('num'))
                    content = match.group('content')
                    # filename
                    content_match = content_compiler.match(content)
                    module = self.target_name
                    if content_match:
                        filename = content_match.group('filename')
                        path = content_match.group('path')
                        module = os.path.basename(path)
                    else:
                        filename = os.path.basename(content)

                    self.file_objs.append(FileObject(module=module, number=num, filename=filename))
                elif self.last_block == BLOCK_SESSION:
                    compiler = re.compile(r"\s*(?P<address>0x[0-9A-Za-z]*)\s+(?P<size>0x[0-9A-Za-z]*)\s+"
                                          r"(?P<segment>\w+)\s+(?P<section>\w+)")
                    match = compiler.match(line)
                    if match:
                        section = Section(address=match.group('address'), size=match.group('size'),
                                          segment=match.group('segment'), section=match.group('section'))
                        self.sections.append(section)
                    else:
                        print 'Parse error: %s' % line
                elif self.last_block == BLOCK_SYMBOLS:
                    compiler = re.compile(r"\s*(?P<address>0x[0-9A-Za-z]*)\s+(?P<size>0x[0-9A-Za-z]*)\s+"
                                          r"\[\s*(?P<file>\d+)\s*\]\s+(?P<name>.+)")
                    match = compiler.match(line)
                    if match:
                        symbol = Symbol(address=match.group('address'), size=match.group('size'),
                                        file_number=int(match.group('file')), name=match.group('name'))
                        self.symbols.append(symbol)
                    else:
                        print 'Parse error: %s' % line

    def __paring_block(self, line):
        compiler = re.compile(r"\s*#\s*(?P<block>[\w\s]*):?\s*(?P<value>.*)")
        match = compiler.match(line)
        if not match:
            return False

        block = match.group('block').strip()
        value = match.group('value').strip()
        blocks = [BLOCK_PATH, BLOCK_ARCH, BLOCK_OBJECT_FILES, BLOCK_SESSION, BLOCK_SYMBOLS, BLOCK_DEAD_STRIPPED_SYMBOLS]
        for b in blocks:
            if block != b:
                continue

            self.last_block = b
            if b == BLOCK_PATH:
                self.path = value
            elif b == BLOCK_ARCH:
                self.arch = value
            break

        return True
