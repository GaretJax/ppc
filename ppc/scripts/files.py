import sys
import os
import argparse

from ppc.utils import iter_files


DEFAULT_EXTS = ['c', 'cc', 'cpp', 'h', 'ph']


def build_parser():
    parser = argparse.ArgumentParser(description='Files indexer for the '
                                     'POP-C++ Posix Checker.')
    parser.add_argument('-e', '--extension', default=DEFAULT_EXTS,
                        action='append', dest='extensions',
                        help='Extensions of the files to add to the database.')
    parser.add_argument('-n', '--not-extension', action='append', default=[],
                        dest='not_exts', help='Extensions of the files to add'
                        ' to the database.')
    parser.add_argument('source', help='Location of the POP-C++ sources to '
                        'analyze.')
    parser.add_argument('files_db', help='Path to the files database to '
                        'generate.')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    srcdir = os.path.realpath(args.source)
    exts = set(args.extensions) - set(args.not_exts)

    with open(args.files_db, 'w') as fh:
        for f in iter_files(srcdir, exts):
            fh.write(f)
            fh.write('\n')


if __name__ == '__main__':
    sys.exit(main())
