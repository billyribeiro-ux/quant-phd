"""Round 6 (M7-d): every number on a card's back must appear in the card's own lesson (rule 10), and the lesson's
text is taken with tags stripped and entities decoded. Prints the cards with a number that is absent from the lesson."""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M7-d")
MOD = ROOT / "course/modules/M/M7"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
texts: dict[str, str] = {}
for lesson in sorted({c["lesson"] for c in cards}):
    raw = (MOD / f"{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    texts[lesson] = re.sub(r"\s+", " ", txt)
num = re.compile(r"(?<![A-Za-z_])-?\d+(?:\.\d+)?(?:/\d+)?")
misses = []
for c in cards:
    body = c["back"]
    for tok in set(num.findall(body)):
        t = tok.lstrip("-")
        if len(t.strip("0.")) == 0:
            continue
        if t not in texts[c["lesson"]]:
            misses.append((c["id"], c["lesson"], tok))
print("cards:", len(cards), "distinct lessons:", sorted(texts))
print("number tokens absent from the card's own lesson:", len(misses))
for m in misses:
    print(*m)
ids = [c["id"] for c in cards]
print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
print("ids missing from the M7-c001..M7-c162 range:", sorted(set(f"M7-c{n:03d}" for n in range(1, 168)) - set(ids)))
fronts = [c["front"] for c in cards]
print("duplicate fronts:", sorted({f for f in fronts if fronts.count(f) > 1}))
print("grades:", sorted({c["grade"] for c in cards}), "non-T without basis:", [c["id"] for c in cards if c["grade"] != "T" and not c.get("basis")])
