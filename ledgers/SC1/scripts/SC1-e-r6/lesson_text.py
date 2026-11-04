"""Extract learner-visible text from a lesson page. Usage: lesson_text.py <page.html>.

Raw '<' inside \\( \\) or \\[ \\] math spans is escaped first, so that the text
the browser would hide (an '<' that opens a fake tag) is printed, and reported
on stderr with its count so the defect is visible.
"""
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "pre", "ol", "ul", "header",
         "table", "dt", "dd", "blockquote", "figcaption", "details", "summary", "figure"}


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in BLOCK:
            self.out.append("\n")
        if tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n## ")
        if tag == "br":
            self.out.append("\n")
        if tag == "li":
            self.out.append("- ")

    def handle_endtag(self, tag):  # type: ignore[no-untyped-def]
        if tag in ("script", "style"):
            self.skip -= 1
            return
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, d):  # type: ignore[no-untyped-def]
        if not self.skip:
            self.out.append(d)


def escape_math(src: str) -> tuple[str, int]:
    count = 0

    def fix(m: re.Match[str]) -> str:
        nonlocal count
        s = m.group(0)
        n = s.count("<")
        count += n
        return s.replace("<", "&lt;")

    out = re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", fix, src, flags=re.S)
    return out, count


if __name__ == "__main__":
    raw = open(sys.argv[1], encoding="utf-8").read()
    fixed, n = escape_math(raw)
    sys.stderr.write(f"raw '<' inside math spans escaped: {n}\n")
    p = P()
    p.feed(fixed)
    txt = "".join(p.out)
    txt = re.sub(r"\n[ \t]*\n+", "\n", txt)
    sys.stdout.write(txt)
