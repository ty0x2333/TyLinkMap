import argparse
from .linkmap import LinkMap


def main(argv=None):
    parser = argparse.ArgumentParser(description='link map tool')
    parser.add_argument('file', help='link map file')
    args = parser.parse_args(argv)

    link_map = LinkMap()
    link_map.paring(args.file)
    for obj in link_map.file_objs:
        print obj
    for section in link_map.sections:
        print section
    for symbol in link_map.symbols:
        print symbol

if __name__ == '__main__':
    main()