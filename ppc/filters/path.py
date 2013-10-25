
from ppc.rendering import filter


@filter('pathlinks')
def pathlinks(path):
    chunks = path.split('/')
    link = ''
    for chunk in chunks[:-1]:
        link += chunk + '/'
        yield chunk, link + 'index.html'
    yield chunks[-1], None
