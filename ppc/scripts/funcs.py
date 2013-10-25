import sys
import os
import glob
import argparse

from lxml import etree
from bs4 import BeautifulSoup
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress
import CppHeaderParser


def build_parser():
    parser = argparse.ArgumentParser(description='Functions indexer for the '
                                     'POP-C++ Posix Checker.')
    parser.add_argument('docdir', help='Location of the Posix documentation to'
                        'analyze.')
    parser.add_argument('funcs_db', help='Path to the funcs database to '
                        'generate.')
    return parser


def get_synopsis(soup):
    synopsis = soup.xpath('//blockquote[@class="synopsis"]//code')
    if not synopsis:
        return []
    return synopsis


def parse(text):
    text = text.replace(u'\xa0', ' ')
    try:
        cppHeader = CppHeaderParser.CppHeader(text, argType='string')
        for func in cppHeader.functions:
            yield func
    except CppHeaderParser.CppParseError as e:
        print e
        raise


def main():
    parser = build_parser()
    args = parser.parse_args()

    parsing_progress = ProgressBar(widgets=[
        ' Parsing documentation  ', Bar(left='[', right=']'), ' ',
        Percentage(), ' (', SimpleProgress(), ') ',
    ])

    writing_progress = ProgressBar(widgets=[
        '        Writing result  ', Bar(left='[', right=']'), ' ',
        Percentage(), ' (', SimpleProgress(), ') ',
    ])

    files = glob.glob(os.path.join(args.docdir, 'functions', '*.html'))
    funcs = set()

    parser = etree.HTMLParser()

    for f in parsing_progress(files):
        with open(f) as fh:
            root = etree.parse(fh, parser)

        synopsis = get_synopsis(root)

        for box in synopsis:
            text = u''.join(box.xpath('.//text()'))

            for func in parse(text):
                funcs.add(func['name'])

    with open(args.funcs_db, 'w') as fh:
        for func in writing_progress(sorted(funcs)):
            fh.write(func)
            fh.write('\n')


if __name__ == '__main__':
    sys.exit(main())
