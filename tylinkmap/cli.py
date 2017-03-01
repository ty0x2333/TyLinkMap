import argparse
from .linkmap import LinkMap
from tabulate import tabulate
import time


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.m_secs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %d ms' % self.m_secs


def main(argv=None):
    parser = argparse.ArgumentParser(description='link map tool')
    parser.add_argument('file', help='link map file')
    parser.add_argument('--desc', action="store_true", help='according to the output module size descending')
    args = parser.parse_args(argv)

    link_map = LinkMap()
    print 'Parsing'
    with Timer(True) as t:
        link_map.paring(args.file)
    print 'Analyze'
    with Timer(True) as t:
        modules = [(k, v) for k, v in link_map.analyze().items()]
        modules.sort(key=lambda tup: tup[1], reverse=args.desc)
    print 'Result'
    print tabulate([(k, link_map.human_size(v)) for k, v in modules], headers=['Module', 'Size'], tablefmt='orgtbl')
    # for obj in link_map.file_objs:
    #     print obj
    # for section in link_map.sections:
    #     print section
    # for symbol in link_map.symbols:
    #     print symbol

if __name__ == '__main__':
    main()