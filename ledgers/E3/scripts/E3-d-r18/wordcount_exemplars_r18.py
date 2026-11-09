"""Word count of each exemplar's memo text on project.html (ruling-free check of the page's stated counts).

Scope: the .memo-text blocks inside each <article class="exemplar">, headings included. Tags are removed with a real HTML
tokenizer (html.parser), not a regex, because the page writes math such as \\(0<\\gamma<1\\) whose '<' is text, not a tag.
Counted as runs of non-whitespace characters. Usage: python3 -I wordcount_exemplars_r18.py <project.html>
"""

import re
import sys
from html.parser import HTMLParser


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


src = open(sys.argv[1], encoding="utf-8").read()
for name in ("exemplar-a", "exemplar-b"):
    start = src.index(f'<article class="exemplar" id="{name}"')
    end = src.index("</article>", start)
    article = src[start:end]
    blocks = re.findall(r'<div class="memo-text">(.*?)</div>', article, flags=re.S)
    parser = Text()
    for block in blocks:
        parser.feed(block)
    text = " ".join(parser.parts)
    print(name, "memo blocks:", len(blocks), "memo words:", len(text.split()), "chars:", len(text))
