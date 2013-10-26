import sys
import re
import os
import argparse
import shutil

from ppc.rendering import build_environment
from ppc.report import generate_file_index, generate_tagsfile, generate_funcs_index
from ppc.utils import grep_files


def build_parser():
    parser = argparse.ArgumentParser(description='POP-C++ Posix Checker.')
    parser.add_argument('source', help='Location of the POP-C++ sources to '
                        'analyze.')
    parser.add_argument('-d', '--posix-doc',
                        help='Location of the Posix documentation.')
    parser.add_argument('funcs_db', help='Path to the functions database.')
    parser.add_argument('files_db', help='Path to the files database.')
    parser.add_argument('report', help='Directory where the report has to be '
                        'stored.')
    return parser


def read_functions_db(path):
    with open(path) as fh:
        funcs = (f.strip() for f in fh)
        return {f: re.compile(r'[^:>\.a-zA-Z0-9_]{}\('.format(f)) for f in funcs}


def read_files_db(path):
    with open(path) as fh:
        return [p.strip() for p in fh]


def main():
    parser = build_parser()
    args = parser.parse_args()

    funcs = read_functions_db(args.funcs_db)
    files = read_files_db(args.files_db)

    #import pprint
    #pprint.pprint(cross_reference)

    if not os.path.exists(args.report):
        os.makedirs(args.report)

    if args.posix_doc:
        shutil.copytree(args.posix_doc, os.path.join(args.report, 'posix_doc'))

    cross_reference = grep_files(args.source, files, funcs)

    env = build_environment()
    generate_funcs_index(env, args.report, cross_reference)
    generate_tagsfile(env, args.report, funcs)
    generate_file_index(env, args.report, args.source, files, cross_reference)


if __name__ == '__main__':
    sys.exit(main())
