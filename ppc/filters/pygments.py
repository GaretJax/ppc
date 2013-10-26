from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

from ppc.rendering import filter


@filter('highlight')
def pygments_highlight(code, tagsfile=None):
    if tagsfile:
        kwargs = {
            'tagsfile': tagsfile,
            'tagurlformat': '%(path)s%(fname)s%(fext)s',
        }
    else:
        kwargs = {}

    formatter = HtmlFormatter(
        linenos='table',
        lineanchors='l',
        anchorlinenos=True,
        **kwargs
    )
    return highlight(code, CppLexer(), formatter)
