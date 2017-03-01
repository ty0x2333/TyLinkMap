import argparse
from .linkmap import LinkMap


def main(argv=None):
    parser = argparse.ArgumentParser(description='link map tool')
    parser.add_argument('file', help='link map file')
    parser.add_argument('--desc', action="store_true", help='according to the output module size descending')
    args = parser.parse_args(argv)

    link_map = LinkMap()
    link_map.paring(args.file)
    modules = [(k, v) for k, v in link_map.analyze().items()]
    modules.sort(key=lambda tup: tup[1], reverse=args.desc)
    for (m, s) in modules:
        print m, link_map.human_size(s)
    # for obj in link_map.file_objs:
    #     print obj
    # for section in link_map.sections:
    #     print section
    # for symbol in link_map.symbols:
    #     print symbol

if __name__ == '__main__':
    main()