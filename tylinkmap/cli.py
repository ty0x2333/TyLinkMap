import argparse
from .linkmap import LinkMap


def main(argv=None):
    parser = argparse.ArgumentParser(description='link map tool')
    parser.add_argument('file', help='link map file')
    args = parser.parse_args(argv)

    link_map = LinkMap()
    link_map.paring(args.file)

if __name__ == '__main__':
    main()