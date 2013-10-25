import os


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

    for path in files:
        path = os.path.join(srcdir, path)
        with open(path) as fh:
            content = fh.read()

        for func, regex in func_pattern.iteritems():
            if regex.search(content) is not None:
                func_occurrences.setdefault(func, []).append(path)
                file_occurrences.setdefault(path, []).append(func)

    return func_occurrences, file_occurrences
