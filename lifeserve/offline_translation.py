import re
import sys
import types
from functools import lru_cache

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString


# Argos currently imports Stanza for sentence splitting even when the packaged
# model does not need its full NLP runtime. This lightweight splitter keeps the
# offline translator free from the optional Torch dependency.
if 'stanza' not in sys.modules:
    stanza = types.ModuleType('stanza')
    stanza.Pipeline = lambda **kwargs: lambda text: types.SimpleNamespace(
        sentences=[types.SimpleNamespace(text=text)]
    )
    sys.modules['stanza'] = stanza

_WHITESPACE = re.compile(r'^(\s*)(.*?)(\s*)$', re.DOTALL)
_TRANSLATABLE_ATTRIBUTES = ('alt', 'placeholder', 'title', 'aria-label')
_SKIP_TAGS = {'script', 'style', 'noscript', 'option'}


@lru_cache(maxsize=4096)
def translate_text(text):
    match = _WHITESPACE.match(text)
    if not match or not re.search(r'[A-Za-z]', match.group(2)):
        return text

    content = match.group(2).strip()
    if not content:
        return text

    try:
        from argostranslate import translate

        translated = translate.translate(content, 'en', 'hi')
    except Exception:
        return text

    return f'{match.group(1)}{translated}{match.group(3)}'


def _is_skipped(node):
    return any(
        getattr(parent, 'name', None) in _SKIP_TAGS
        or getattr(parent, 'get', lambda *args: None)('translate') == 'no'
        for parent in [node, *node.parents]
    )


def _inside_language_switcher(node):
    return any(
        'language-switcher' in parent.get('class', [])
        for parent in node.parents
        if getattr(parent, 'name', None)
    )


def translate_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    for text_node in soup.find_all(string=True):
        if (
            isinstance(text_node, NavigableString)
            and not isinstance(text_node, (Comment, Doctype))
            and not _is_skipped(text_node)
        ):
            if not _inside_language_switcher(text_node):
                text_node.replace_with(translate_text(str(text_node)))

    for element in soup.find_all(True):
        if _is_skipped(element):
            continue
        if _inside_language_switcher(element):
            continue
        for attribute in _TRANSLATABLE_ATTRIBUTES:
            if element.has_attr(attribute):
                element[attribute] = translate_text(element[attribute])

    return str(soup)


class OfflineTranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.LANGUAGE_CODE != 'hi' or response.get('Content-Type', '').split(';')[0] != 'text/html':
            return response

        if not response.streaming:
            response.content = translate_html(response.content.decode(response.charset or 'utf-8')).encode(response.charset or 'utf-8')
            response.headers.pop('Content-Length', None)

        return response
