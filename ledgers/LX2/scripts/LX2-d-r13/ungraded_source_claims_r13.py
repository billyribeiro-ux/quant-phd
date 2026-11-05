"""Round 13: list text nodes of a lesson that sit OUTSIDE every claim span (class 'claim') and
that attribute content to a statute, opinion, Code or letter (locator-like words). Each hit must
either be a non-attributive sentence or sit in a claim span. Usage: python3 -I <script> <lesson.html>"""
import sys, re
from html.parser import HTMLParser
PAT = re.compile(r"\b(section|sections|§|Section \d|Act|Code|Standard|Dirks|O'Hagan|opinion|letter|attachment|SR 26-2|statute|statutory|the text says|states|provides|says)\b", re.I)
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col", "area", "base", "embed", "param", "track"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # entries: (tag, is_claim, is_skip)
        self.hits = []
        self.line = 0
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        claim = 'claim' in (a.get('class') or '').split()
        skip = tag in ('script', 'style', 'pre', 'code', 'svg', 'math')
        self.stack.append((tag, claim, skip))
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, d):
        if any(s for _, _, s in self.stack):
            return
        if any(c for _, c, _ in self.stack):
            return
        for sent in re.split(r"(?<=[.;:])\s+", d.strip()):
            if PAT.search(sent) and len(sent) > 25:
                self.hits.append((self.getpos()[0], sent.strip()))
p = P()
p.feed(open(sys.argv[1], encoding="utf-8").read())
for ln, s in p.hits:
    print(f"L{ln}: {s[:260]}")
print("candidates:", len(p.hits))
