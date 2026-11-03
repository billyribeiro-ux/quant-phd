"""Write cleaned lesson text (code blocks replaced by a marker, expected outputs kept, TeX kept) for card reading.

Uses html.parser (not a tag regex), because TeX inside the pages contains '<' characters.
Usage: python3 -I clean_lessons.py <checkout> <outdir>
"""
import html.parser
import pathlib
import re
import sys


class Text(html.parser.HTMLParser):
    BREAK = {"p", "li", "h1", "h2", "h3", "h4", "div", "tr", "dt", "dd", "section", "details", "summary", "pre",
             "figcaption", "table", "ul", "ol", "header", "br"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "nav"):
            self.skip += 1
        if tag in self.BREAK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "nav"):
            self.skip = max(0, self.skip - 1)
        if tag in self.BREAK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


base = pathlib.Path(sys.argv[1]) / "course/modules/M/M2"
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for page in sorted(base.glob("L*.html")):
    raw = page.read_text(encoding="utf-8")
    raw = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', "\n[CODE BLOCK OMITTED]\n", raw, flags=re.S)
    p = Text()
    p.feed(raw)
    lines = [" ".join(l.split()) for l in "".join(p.out).split("\n")]
    (out / (page.stem + ".txt")).write_text("\n".join(l for l in lines if l) + "\n", encoding="utf-8")
print("ok")
