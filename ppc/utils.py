import os
from collections import Counter

from .progress import get_label_progress


def sibling_file(path, filename):
    return os.path.join(os.path.dirname(path), filename)


def get_extensions(srcdir):
    exts = set()
    for root, dirs, files in os.walk(srcdir):
        files = (f.rsplit('.') for f in files)
        files = (f[1] for f in files if len(f) == 2)
        exts.update(files)

    return exts


def iter_files(srcdir, exts):
    for root, dirs, files in os.walk(srcdir):
        for f in files:
            split = f.rsplit('.')

            if len(split) != 2:
                continue

            if split[1] not in exts:
                continue

            yield os.path.join(root, f)[len(srcdir) + 1:]


def grep_files(srcdir, files, func_pattern):
    func_occurrences = {}
    file_occurrences = {}

    search_progress = get_label_progress('Cross referencing functions:')

    for func in func_pattern:
        func_occurrences[func] = {}

    for path in search_progress(files):
        abspath = os.path.join(srcdir, path)
        with open(abspath) as fh:
            content = fh.read()

        file_occurrences[path] = []

        func_lines = {}

        for func, regex in func_pattern.iteritems():
            for match in regex.finditer(content):
                line = content.count('\n', 0, match.start()) + 1
                func_lines.setdefault(func, []).append(line)

        for func, lines in func_lines.iteritems():
            func_occurrences[func][path] = lines

        file_occurrences[path] = func_lines

    return func_occurrences, file_occurrences
