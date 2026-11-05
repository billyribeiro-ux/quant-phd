"""Round 7: banned phrases, process words, scope words, counts, word counts and hours attributes on slice pages (run with -I)."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(".").resolve()
PAGES = ["course/modules/PC/PC3/index.html", "course/modules/PC/PC3/L01.html",
         "course/modules/PC/PC3/L02.html", "course/modules/PC/PC3/L03.html"]
TWINS = ["tests/labs/PC3/lab-PC3-L01-1.py", "tests/labs/PC3/lab-PC3-L02-1.py", "tests/labs/PC3/lab-PC3-L03-1.py"]


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
PROCESS = ["build", "builder", "round", "verifier", "requests", "unit report", "fixer", "ledger"]
SCOPE = ["only", "all ", "always", "every", "any ", "same", "drives", "exactly", "never"]
for page in PAGES:
    raw = (ROOT / page).read_text(encoding="utf-8")
    t = Text()
    t.feed(raw)
    text = " ".join(t.parts)
    low = text.lower()
    print(f"== {page}: visible chars {len(text)}")
    for b in BANNED:
        n = low.count(b.lower())
        if n:
            print(f"  banned '{b}': {n} hit(s)")
    for w in PROCESS:
        for m in re.finditer(r"\b" + re.escape(w), low):
            s = max(0, m.start() - 60)
            print(f"  process word '{w}': ...{text[s:m.end() + 40]!r}")
    # raw HTML (incl. code) process words
    for m in re.finditer(r"\bround\b", raw, re.I):
        line = raw.count("\n", 0, m.start()) + 1
        print(f"  raw 'round' at line {line}: {raw[max(0,m.start()-50):m.end()+30]!r}")
    # problem and solution counts
    print(f"  problems: {len(re.findall(r'class=\"problem\"', raw))}, solutions: {len(re.findall(r'details class=\"solution\"', raw))}")
    print(f"  quiz items: {len(re.findall(r'<li class=\"item\"', raw))}, misconceptions: {len(re.findall(r'class=\"misconception\"', raw))}")
    print(f"  data-hours: {re.findall(r'data-hours[^=]*=\"[^\"]*\"', raw)}")
    wm = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if wm:
        wt = re.sub(r"<[^>]+>", " ", wm.group(1))
        print(f"  why-it-matters words: {len(wt.split())}")
    # scope words in body prose (lower-case whole words), counted for review
    for w in ["only", "every", "all", "always", "any", "same", "exactly", "never"]:
        print(f"  scope '{w}': {len(re.findall(r'\\b' + w + r'\\b', low))}")
for tw in TWINS:
    src = (ROOT / tw).read_text(encoding="utf-8")
    print(f"== {tw}: open/read/http hits: {len(re.findall(r'open\\(|read_text|urllib|requests|http', src))}; 'round' hits: {len(re.findall(r'round', src, re.I))}")
