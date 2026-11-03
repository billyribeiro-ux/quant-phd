"""Extract readable text from a lesson or project HTML page (keeps TeX source, block titles, ids).

Usage: python3 -I extract_text.py <in.html> <out.txt>
"""
import html.parser
import sys


class T(html.parser.HTMLParser):
    BREAK = {"p", "li", "h1", "h2", "h3", "h4", "div", "tr", "dt", "dd", "section", "details", "summary", "pre", "figure", "figcaption", "ul", "ol", "table", "br", "caption", "thead", "tbody"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "svg", "nav", "header"):
            if tag in ("script", "style", "svg"):
                self.skip += 1
                return
        if tag in self.BREAK:
            self.out.append("\n")
        if tag == "h2" or tag == "h3":
            self.out.append("\n## ")
        if "id" in a and a["id"]:
            self.out.append(f"[#{a['id']}]")
        if tag == "span" and "data-grade" in a:
            self.out.append(f"[GRADE {a['data-grade']}]")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in self.BREAK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip == 0:
            self.out.append(data)


def main():
    p = T()
    p.feed(open(sys.argv[1], encoding="utf-8").read())
    text = "".join(p.out)
    lines = [" ".join(l.split()) for l in text.split("\n")]
    out = "\n".join(l for l in lines if l)
    open(sys.argv[2], "w", encoding="utf-8").write(out + "\n")


if __name__ == "__main__":
    main()
