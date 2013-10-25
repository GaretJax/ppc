import os
import glob

from jinja2 import Environment, FileSystemLoader

from .utils import sibling_file


def build_environment():
    loader = FileSystemLoader(sibling_file(__file__, 'templates'))
    env = Environment(loader=loader)
    load_filters(env)
    return env


def load_filters(env):
    from ppc import filters
    package_path = filters.__file__
    modules = sibling_file(package_path, '*.py')

    for path in glob.glob(modules):
        filename = os.path.basename(path)
        if filename.startswith('_'):
            continue
        globals_dict = {}
        execfile(path, globals_dict)
        for k, v in globals_dict.iteritems():
            if isinstance(v, Filter):
                v.register(env)


class Filter(object):
    def __init__(self, name):
        self._name = name

    def __call__(self, func):
        self._func = func
        return self

    def register(self, env):
        env.filters[self._name] = self._func

filter = Filter

def render_to_file(env, template, outdir, output_file, context):
    dest = os.path.join(outdir, output_file)
    context['_path_depth'] = output_file.count('/')
    context['_base'] = '/'.join(['..'] * context['_path_depth'])

    d = os.path.dirname(dest)
    if not os.path.exists(d):
        os.makedirs(d)
    template = env.get_template(template)
    template.stream(context).dump(dest)
