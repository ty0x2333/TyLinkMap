import argparse
from .linkmap import LinkMap
from tabulate import tabulate
import logging
import time


class Timer(object):
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.m_secs = self.secs * 1000  # millisecs
        logging.debug('elapsed time: %d ms' % self.m_secs)

SUFFIXES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def human_size(nbytes):
    if nbytes == 0: return '0 B'
    size = nbytes
    i = 0
    while size >= 1024 and i < len(SUFFIXES) - 1:
        size /= 1024.
        i += 1
    f = ('%.2f' % size).rstrip('0').rstrip('.')
    return '%s %s' % (f, SUFFIXES[i])


def main(argv=None):
    parser = argparse.ArgumentParser(description='link map tool')
    parser.add_argument('file', help='link map file')
    parser.add_argument('--desc', action="store_true", help='according to the output module size descending')
    parser.add_argument('-v', '--verbose', action="store_true", dest="verbose", help="show more debugging information")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format='%(message)s')

    link_map = LinkMap()
    logging.debug('Parsing...')
    with Timer() as t:
        link_map.paring(args.file)
    logging.debug('Analyzing...')
    with Timer() as t:
        modules = [(k, v) for k, v in link_map.analyze().items()]
        modules.sort(key=lambda tup: tup[1], reverse=args.desc)
    logging.debug('Result')
    logging.info(tabulate([(k, human_size(v)) for k, v in modules],
                          headers=['Module', 'Size'],
                          tablefmt='orgtbl'))
    logging.info('Total: %s' % human_size(sum([m[1] for m in modules])))
    # for obj in link_map.file_objs:
    #     print obj
    # for section in link_map.sections:
    #     print section
    # for symbol in link_map.symbols:
    #     print symbol

if __name__ == '__main__':
    main()