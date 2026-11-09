"""Structural and banned-phrase scan for M3 lessons L04-L06 (verifier script, round 1)."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "it can be shown that", "in practice", "robust", "stable", "always", "every matrix",
    "generic", "typically", "almost always", "...", "…",
]


class Words(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "why-it-matters") in attrs:
            pass

    def handle_data(self, data):
        self.buf.append(data)


for name in ["L04", "L05", "L06"]:
    path = ROOT / "course/modules/M/M3" / f"{name}.html"
    text = path.read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    why = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
    why = re.sub(r"\\\((.*?)\\\)", r"x", why)
    print(f"== {name}")
    print("data-hours:", re.search(r'data-hours="(\d+)"', text).group(1))
    print("why-it-matters words (tags stripped, math as one token):", len(why.split()))
    print("problems:", len(re.findall(r'<div class="problem"', text)),
          "solutions:", len(re.findall(r'<details class="solution"', text)))
    for tier in ["mechanics", "proof", "empirical", "research"]:
        print(f"  tier {tier}:", len(re.findall(rf'data-tier="{tier}".*?(?=data-tier=|</section>)', text, re.S)) and
              len(re.findall(r'class="problem"', re.search(rf'data-tier="{tier}".*?(?=data-tier="|</section>)', text, re.S).group(0))))
    print("quiz items:", len(re.findall(r'<li class="item"', text)),
          "correct-marked mc:", len(re.findall(r'data-correct', text)))
    print("misconceptions:", len(re.findall(r'class="misconception"', text)))
    print("key-results rows:", len(re.findall(r'<tr><td>', text)))
    print("dfn:", re.findall(r'<dfn id="([^"]+)" data-concept="([^"]+)"', text))
    print("concept links:", sorted(set(re.findall(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)"', text))))
    print("claim grades:", sorted(set(re.findall(r'data-grade="([TABCDX])"', text))))
    low = text.lower()
    for b in BANNED:
        hits = [i for i in range(len(low)) if low.startswith(b.lower(), i)]
        if hits:
            lines = sorted({text.count("\n", 0, i) + 1 for i in hits})
            print(f"  BANNED HIT {b!r} at lines {lines[:20]}")
    print("")
