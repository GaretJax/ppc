import sys
import re
import os
import argparse

from ppc.rendering import build_environment
from ppc.report import generate_file_index


def build_parser():
    parser = argparse.ArgumentParser(description='POP-C++ Posix Checker.')
    parser.add_argument('source', help='Location of the POP-C++ sources to '
                        'analyze.')
    parser.add_argument('funcs_db', help='Path to the functions database.')
    parser.add_argument('files_db', help='Path to the files database.')
    parser.add_argument('report', help='Directory where the report has to be '
                        'stored.')
    return parser


def read_functions_db(path):
    with open(path) as fh:
        funcs = (f.strip() for f in fh)
        return {f: re.compile(r'[^a-z0-9]{}\('.format(f)) for f in funcs}


def read_files_db(path):
    with open(path) as fh:
        return [p.strip() for p in fh]


def main():
    parser = build_parser()
    args = parser.parse_args()

    #funcs = read_functions_db(args.funcs_db)
    files = read_files_db(args.files_db)

    if not os.path.exists(args.report):
        os.makedirs(args.report)

    env = build_environment()
    generate_file_index(env, args.report, args.source, files)


if __name__ == '__main__':
    sys.exit(main())
