"""For every AC1 card: each 'Definition/Proposition/Theorem/Corollary/Remark N.M' cited in its back must exist as a labelled
block in the card's own lesson (for L-pages) or in the cited lesson text named in the card; prints the misses."""

import json
import re
import sys

ROOT = "/tmp/verify15-AC1-d/course/modules/AC/AC1/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
pat = re.compile(r"(Definition|Proposition|Theorem|Corollary|Remark|Lemma) (\d+\.\d+)")
texts = {}
for c in cards:
    lesson = c["lesson"]
    if lesson not in texts:
        texts[lesson] = open(ROOT + lesson + ".html", encoding="utf-8").read()
    for kind, num in pat.findall(c["back"] + " " + c["front"]):
        if f"{kind} {num}" not in texts[lesson]:
            print("MISS", c["id"], lesson, f"{kind} {num}")
print("checked", len(cards), "cards")
sys.exit(0)
