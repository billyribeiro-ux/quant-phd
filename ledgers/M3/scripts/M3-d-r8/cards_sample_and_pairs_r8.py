"""Round-8 verifier (M3 slice d): (1) seeded sample of 20 cards printed with their lesson anchor; (2) every card pair at token
Jaccard 0.40 or more, with both fronts. Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/cards_sample_and_pairs_r8.py
"""

import html
import itertools
import json
import random
import re
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "course/modules/M/M3"
cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))


def plain(p):
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


L = {f"L{n:02d}": plain(BASE / f"L{n:02d}.html") for n in range(1, 10)}
print("== (1) seeded sample of 20 (random.Random(20261104))")
for c in random.Random(20261104).sample(cards, 20):
    lt = L[c["lesson"]]
    m = re.search(r"(Definition|Proposition|Theorem|Lemma|Fact|Remark|Example|Exercise|Lab|Misconception|Corollary)\s+\d[\d.a-z()]*",
                  c["back"] + " " + c["front"])
    anchor = ""
    if m and m.group(0) in lt:
        k = lt.find(m.group(0))
        anchor = lt[k:k + 200]
    print(c["id"], c["lesson"], c.get("grade"), "\n  F:", c["front"][:200], "\n  B:", c["back"][:240], "\n  LESSON:", anchor)
print("== (2) pairs at Jaccard >= 0.40 with fronts")
allc = [(c["id"], c["lesson"], (c["front"] + " " + c["back"]).lower(), c["front"]) for c in cards]
pairs = []
for (a, la, ta, fa), (b, lb, tb, fb) in itertools.combinations(allc, 2):
    sa, sb = set(re.findall(r"[a-z0-9]+", ta)), set(re.findall(r"[a-z0-9]+", tb))
    j = len(sa & sb) / max(1, len(sa | sb))
    if j >= 0.40:
        pairs.append((round(j, 2), a, b, fa[:110], fb[:110]))
pairs.sort(reverse=True)
print(len(pairs), "pairs")
for p in pairs:
    print(p[0], p[1], p[2], "|", p[3], "|", p[4])
