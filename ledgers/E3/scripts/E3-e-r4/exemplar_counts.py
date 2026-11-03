"""Count the words of each exemplar memo on project.html (round 4, slice e).

Rule quoted on the page: runs of characters between spaces, in the memo text with its tags removed, headings included.
Tags are removed with html.parser (a '<' that does not open a tag, as in \\(0<\\gamma<1\\), stays as text).
Usage: python3 -I exemplar_counts.py <checkout>
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def words(markup: str) -> int:
    parser = Text()
    parser.feed(markup)
    parser.close()
    return len(" ".join(parser.parts).split())


root = Path(sys.argv[1])
text = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for name in ("exemplar-a", "exemplar-b"):
    start = text.index(f'<article class="exemplar" id="{name}"')
    block = text[start : text.index("</article>", start)]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>', block, flags=re.S)
    per_memo = [words(m) for m in memos]
    body = [words(re.sub(r"<h5>.*?</h5>", " ", m, flags=re.S)) for m in memos]
    print(name, "memos", len(memos), "words incl. headings", sum(per_memo), "body only", sum(body))
    print(name, "per memo incl. headings", per_memo)
    print(name, "whole article text", words(block))

# Variants of the stated rule, for the exemplar memos only (headings included).
# (a) tags removed with no inserted space, split on whitespace; (b) tags replaced by a space, split on whitespace.
for name in ("exemplar-a", "exemplar-b"):
    start = text.index(f'<article class="exemplar" id="{name}"')
    block = text[start : text.index("</article>", start)]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>', block, flags=re.S)
    tags_removed = 0
    tags_spaced = 0
    for memo in memos:
        parser = Text()
        parser.feed(memo)
        parser.close()
        tags_removed += len("".join(parser.parts).split())
        tags_spaced += len(" ".join(parser.parts).split())
    print(name, "variant (a) tags removed, whitespace split:", tags_removed,
          "| variant (b) tags as spaces, whitespace split:", tags_spaced)
