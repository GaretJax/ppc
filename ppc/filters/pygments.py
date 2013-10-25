from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

from ppc.rendering import filter


@filter('highlight')
def pygments_highlight(code):
    formatter = HtmlFormatter(
        linenos='table',
        lineanchors='l',
        anchorlinenos=True,
        tagsfile='tags',
        tagurlformat='%(fname)s.html'
    )
    return highlight(code, CppLexer(), formatter)
