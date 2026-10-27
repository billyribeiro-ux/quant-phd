"""Round-28 part C: re-run tools/add_reference.py describe() (line 72-74) on a book with no container (admitted by
ISBN) and on a journal article. Run: python -I describe_check_C.py <checkout>"""
import sys

sys.path.insert(0, f"{sys.argv[1]}/tools")
import add_reference as ar  # noqa: E402
from refs.crossref import Author, Work  # noqa: E402

book = Work(doi="", type="book", title="A Title", authors=(Author(family="Smith", given="J"),), container=(),
            volume=None, issue=None, pages=None, years=frozenset({1995}), year=1995,
            isbn=("9780000000001",), publisher="Pub")
article = Work(doi="10.1/x", type="journal-article", title="A Title", authors=(Author(family="Smith", given="J"),),
               container=("Journal",), volume="50", issue="1", pages="1-2", years=frozenset({1995}), year=1995,
               isbn=(), publisher=None)
print("book    :", repr(ar.describe(book)))
print("article :", repr(ar.describe(article)))
