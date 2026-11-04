"""Print an HTML lesson as numbered plain text lines (stdlib only). Usage: textify.py <file.html>"""
import html.parser
import sys


class T(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "div", "section", "dt", "dd", "summary"):
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


p = T()
with open(sys.argv[1], encoding="utf-8") as fh:
    p.feed(fh.read())
text = "".join(p.out)
for n, line in enumerate(text.split("\n"), 1):
    if line.strip():
        print(f"{n:4d}| {line.strip()}")
