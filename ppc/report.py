import os

from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter

from .rendering import render_to_file


def generate_stylesheet(outdir, stylename='colorful'):
    stylesheet = os.path.join(outdir, 'pygments.css')
    with open(stylesheet, 'w') as fh:
        style = get_style_by_name(stylename)
        formatter = HtmlFormatter(style=style)
        fh.write(formatter.get_style_defs())


def generate_file_index(env, outdir, srcdir, files):
    generate_stylesheet(outdir)
    srcdir = os.path.realpath(srcdir)

    tree = {}

    for path in files[:20]:
        with open(os.path.join(srcdir, path)) as fh:
            content = fh.read()

        tree.setdefault(os.path.dirname(path), set()).add((os.path.basename(path), 0))
        _path = path.split('/')[:-1]
        while _path:
            f = _path[-1]
            del _path[-1]
            tree.setdefault('/'.join(_path), set()).add((f, 1))

        try:
            render_to_file(
                env, 'file.html', outdir,
                os.path.join('files', path + '.html'),
                {'path': path, 'code': content}
            )
        except Exception as e:
            print file, e
            pass

    for k, v in tree.iteritems():
        render_to_file(
            env, 'file_index.html', outdir,
            os.path.join('files', k, 'index.html'),
            {'path': k, 'files': sorted(v)})
