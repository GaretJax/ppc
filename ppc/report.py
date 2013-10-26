import os

from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter

from .rendering import render_to_file
from .progress import get_label_progress


def generate_stylesheet(outdir, stylename='colorful'):
    stylesheet = os.path.join(outdir, 'pygments.css')
    with open(stylesheet, 'w') as fh:
        style = get_style_by_name(stylename)
        formatter = HtmlFormatter(style=style)
        fh.write(formatter.get_style_defs())


def generate_funcs_index(env, outdir, cross_reference):
    context = {
        'funcs': cross_reference[0],
    }
    render_to_file(env, 'funcs_index.html', outdir, 'funcs/index.html', context)


def generate_tagsfile(env, outdir, funcs):
    render_to_file(env, 'tags.txt', outdir, 'tags',
                   {'funcs': sorted(funcs.keys())})


def generate_file_index(env, outdir, srcdir, files, cross_reference):
    generate_stylesheet(outdir)
    srcdir = os.path.realpath(srcdir)

    tree = {}

    generation_progress = get_label_progress('Generating source files:')

    for path in generation_progress(files):
        with open(os.path.join(srcdir, path)) as fh:
            content = fh.read()

        tree.setdefault(os.path.dirname(path), set()).add((os.path.basename(path), 0))
        _path = path.split('/')[:-1]
        while _path:
            f = _path[-1]
            del _path[-1]
            tree.setdefault('/'.join(_path), set()).add((f, 1))

        context = {
            'path': path,
            'code': content,
            'report_path': outdir,
            'funcs': cross_reference[1][path],
        }

        try:
            render_to_file(env, 'file.html', outdir,
                           os.path.join('files', path + '.html'), context)
        except Exception as e:
            print path, e
            pass

    for k, v in tree.iteritems():
        render_to_file(
            env, 'file_index.html', outdir,
            os.path.join('files', k, 'index.html'),
            {'path': k, 'files': sorted(v)})
