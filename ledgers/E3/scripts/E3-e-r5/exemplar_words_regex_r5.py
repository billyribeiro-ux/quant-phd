r"""Why a regex tag stripper gives 435 words for Exemplar B, while a browser-faithful parse gives 582 (round 5).

The raw text of the memo contains a literal '<' in math source: '\(0<\gamma<1\)'. A regex such as <[^>]+> treats
'<\gamma<1\) ... >' as one tag and deletes the text between, so it under-counts. HTMLParser (what a browser does) keeps it.
usage: python -I exemplar_words_regex_r5.py <project.html>
"""

import html
import pathlib
import html.parser
import re
import sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
s = src.index('<article class="exemplar" id="exemplar-b"')
e = src.index("</article>", s)
memo = "".join(re.findall(r'<div class="memo-text">(.*?)</div>', src[s:e], flags=re.S))
regex_text = html.unescape(re.sub(r"<[^>]+>", "", memo))
print("regex tag stripper, whitespace runs:", len(regex_text.split()))


class T(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


p = T()
p.feed(memo)
print("HTMLParser (browser-faithful), whitespace runs:", len("".join(p.parts).split()))
print("raw '<' characters in the memo:", memo.count("<"))
