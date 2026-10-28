"""List every number in each AC4 exemplar memo-text block (argv[1] = project.html) with the sentence it sits in."""
import re
import sys
from html.parser import HTMLParser

class Memo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.blocks = []
        self.cur = None
        self.stack = []
        self.exemplar = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "article" and "exemplar" in (a.get("class") or ""):
            self.exemplar = a.get("id")
        if tag == "div" and "memo-text" in (a.get("class") or ""):
            self.cur = [self.exemplar, ""]
            self.depth = 1
        elif self.cur is not None and tag == "div":
            self.depth += 1
    def handle_endtag(self, tag):
        if self.cur is not None and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.blocks.append(tuple(self.cur))
                self.cur = None
    def handle_data(self, data):
        if self.cur is not None:
            self.cur[1] += data

p = Memo()
p.feed(open(sys.argv[1], encoding="utf-8").read())
for ex, text in p.blocks:
    print("==", ex, "words:", len(text.split()))
    for sent in re.split(r"(?<=[.!?])\s+", " ".join(text.split())):
        nums = re.findall(r"[+−\-]?\d[\d,\.]*%?", sent)
        if nums:
            print("  ", nums, "|", sent[:150])
