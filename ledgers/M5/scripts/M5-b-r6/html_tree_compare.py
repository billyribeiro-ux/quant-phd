"""Compare the HTML token stream (tags, attributes, unescaped text) of two revisions of each slice page.

Text is merged across entity boundaries, so '&lt;' in text equals a raw '<' in text. Markup must be identical:
a '<' that opened a tag in the old revision must still open the same tag in the new one.
"""
import subprocess
from html.parser import HTMLParser

REPO = "/Users/billyribeiro/.fanout/wt/verifyS6-M5-b"
OLD = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
NEW = "e896b7a4"


class Tok(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
    def _text(self, s):
        if self.out and self.out[-1][0] == "data":
            self.out[-1] = ("data", self.out[-1][1] + s)
        else:
            self.out.append(("data", s))
    def handle_starttag(self, tag, attrs):
        self.out.append(("start", tag, tuple(attrs)))
    def handle_startendtag(self, tag, attrs):
        self.out.append(("startend", tag, tuple(attrs)))
    def handle_endtag(self, tag):
        self.out.append(("end", tag))
    def handle_data(self, data):
        self._text(data)
    def handle_comment(self, data):
        self.out.append(("comment", data))
    def handle_decl(self, data):
        self.out.append(("decl", data))


def tokens(rev, path):
    src = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True, cwd=REPO).stdout
    p = Tok()
    p.feed(src)
    p.close()
    return p.out


for path in ("course/modules/M/M5/L05.html", "course/modules/M/M5/L06.html", "course/modules/M/M5/L07.html"):
    a, b = tokens(OLD, path), tokens(NEW, path)
    markup_a = [t for t in a if t[0] != "data"]
    markup_b = [t for t in b if t[0] != "data"]
    print(f"{path}: markup tokens old={len(markup_a)} new={len(markup_b)} identical={markup_a == markup_b}")
    text_a = [t for t in a if t[0] == "data"]
    text_b = [t for t in b if t[0] == "data"]
    diffs = [i for i, (x, y) in enumerate(zip(text_a, text_b)) if x != y]
    print(f"  text chunks old={len(text_a)} new={len(text_b)} differing chunk indexes={len(diffs)}")
    # Which chunks differ, shown as the first differing character
    for i in diffs:
        x, y = text_a[i][1], text_b[i][1]
        k = next((j for j, (c, d) in enumerate(zip(x, y)) if c != d), min(len(x), len(y)))
        print(f"   chunk {i}: old[{k}:]={x[k:k+60]!r} new[{k}:]={y[k:k+60]!r}")
