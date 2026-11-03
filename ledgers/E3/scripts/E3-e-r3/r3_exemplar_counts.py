"""Round 3: word counts of the exemplar memos, by a real HTML parser (not regex), runs of characters between spaces.

Counted under three conventions: (1) tags removed, text kept, headings included (the page's stated method);
(2) as (1) but headings (h5) excluded; (3) as (1) with TeX math spans \\( ... \\) and \\[ ... \\] counted as one token each.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-e/course/modules/E/E3/project.html").read_text(encoding="utf-8")


class Memo(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.blocks = []
        self.cur = None
        self.in_h5 = False
        self.h5_text = []
        self.all_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "div" and dict(attrs).get("class") == "memo-text":
            self.depth = 1
            self.cur = []
            self.blocks.append((self.cur, []))
            return
        if self.depth and tag == "div":
            self.depth += 1
        if self.depth and tag == "h5":
            self.in_h5 = True

    def handle_endtag(self, tag):
        if self.depth and tag == "div":
            self.depth -= 1
        if self.depth and tag == "h5":
            self.in_h5 = False

    def handle_data(self, data):
        if self.depth:
            self.cur.append(data)
            if self.in_h5:
                self.blocks[-1][1].append(data)


def count(s):
    return len(s.split())


def analyse(article_id):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % article_id, PAGE, re.S).group(0)
    m = Memo()
    m.feed(art)
    per_all, per_noh5, per_math = [], [], []
    for text_parts, h5_parts in m.blocks:
        text = "".join(text_parts)
        h5 = "".join(h5_parts)
        per_all.append(count(text))
        per_noh5.append(count(text.replace(h5, " ")))
        math_spans = re.findall(r"\\\((.*?)\\\)", text, re.S)
        without = re.sub(r"\\\((.*?)\\\)", " MATH ", text, flags=re.S)
        per_math.append(count(without))
    return per_all, per_noh5, per_math


for art in ("exemplar-a", "exemplar-b"):
    a, n, mth = analyse(art)
    print(art, "blocks", len(a))
    print("  (1) headings included, per block", a, "total", sum(a))
    print("  (2) headings excluded, per block", n, "total", sum(n))
    print("  (3) TeX spans as one token, per block", mth, "total", sum(mth))
