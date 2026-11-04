"""Word counts of the two rubric exemplars on project.html (round 5).

Counts runs of characters between spaces, headings included, in the exemplar's text with tags removed,
under two tag rules: tags removed (replaced by nothing) and tags replaced by a space.
"""
import html.parser
import re
import sys


class Text(html.parser.HTMLParser):
    def __init__(self, sep: str) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.sep = sep

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self.sep)

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(self.sep)

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def exemplar_html(src: str, ident: str) -> str:
    start = src.index(f'<article class="exemplar" id="{ident}"')
    end = src.index("</article>", start)
    return src[start:end]


def main() -> None:
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    for ident in ("exemplar-a", "exemplar-b"):
        chunk = exemplar_html(src, ident)
        # the memo text only: the annotation <aside> and the verdict paragraph are excluded
        memo = re.findall(r'<div class="memo-text">(.*?)</div>', chunk, flags=re.S)
        body = "\n".join(memo)
        counts = []
        for sep in ("", " "):
            p = Text(sep)
            p.feed(body)
            text = "".join(p.parts)
            counts.append(len(text.split()))
        # also: whole article including verdict paragraph and annotations (for reference)
        p = Text(" ")
        p.feed(chunk)
        whole = len("".join(p.parts).split())
        print(ident, "memo words (tags removed, tags as nothing):", counts[0], "| tags as spaces:", counts[1],
              "| whole article incl. verdict and annotations, tags as spaces:", whole)


main()
