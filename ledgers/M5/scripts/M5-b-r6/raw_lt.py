"""Find raw '<' characters in the slice pages that the HTML parser would not treat as a tag start.

A raw '<' followed by a letter, '/', '!' or '?' opens markup (a tag or a comment); any other raw '<' is text.
Also reports every '<' that opens a start tag whose name is not in the HTML vocabulary (a math '<' followed by a letter).
"""
import re
import sys
from html.parser import HTMLParser

VOCAB = {
    "a", "abbr", "article", "aside", "b", "blockquote", "body", "br", "button", "canvas", "caption", "code", "col",
    "colgroup", "dd", "details", "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "footer", "form",
    "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "i", "iframe", "img", "input", "label", "legend",
    "li", "link", "main", "meta", "nav", "noscript", "ol", "optgroup", "option", "p", "pre", "script", "section",
    "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template",
    "textarea", "tfoot", "th", "thead", "title", "tr", "u", "ul", "var", "svg", "path", "g", "circle", "line", "rect",
    "text", "desc", "polyline", "polygon", "defs", "marker", "tspan", "use", "mi", "mo", "mn", "math", "mrow", "msup",
    "mfrac", "mtext", "mspace", "msub", "mstyle", "mover", "munder", "msqrt", "mtable", "mtr", "mtd", "semantics",
    "annotation", "image", "clippath", "lineargradient", "stop", "ellipse", "foreignobject", "pattern", "symbol",
    "mroot", "menclose", "mpadded", "mphantom", "mmultiscripts", "none", "mtd", "munderover", "msubsup", "mi",
    "video", "audio", "track", "picture", "output", "progress", "meter", "address", "hgroup", "search", "menu", "base",
    "map", "area", "q", "cite", "time", "mark", "ruby", "rt", "rp", "bdi", "bdo", "wbr", "del", "ins", "s", "kbd",
    "samp", "data", "dialog", "object", "param", "embed", "frame", "frameset", "noframes", "colgroup", "center",
}
PATH = sys.argv[1]
src = open(PATH, encoding="utf-8").read()
lines = src.split("\n")

raw = []
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"<", line):
        nxt = line[m.end():m.end() + 1]
        if nxt and (nxt.isalpha() or nxt in "/!?"):
            continue  # markup start: handled by the parser scan below
        raw.append((i, nxt or "EOL"))

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOCAB:
            self.bad.append((self.getpos()[0], tag))
    def handle_startendtag(self, tag, attrs):
        if tag not in VOCAB:
            self.bad.append((self.getpos()[0], tag))

s = Scan()
s.feed(src)
print(f"{PATH}: raw '<' not starting markup = {len(raw)} on lines {sorted({l for l, _ in raw})}")
print(f"{PATH}: raw '<' followed by a letter, '/', '!' or '?' (parser-visible markup) with a non-HTML name = {len(s.bad)} : {s.bad[:20]}")
