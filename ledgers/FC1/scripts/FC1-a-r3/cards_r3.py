"""Round 3: cards of L01-L03 (cards.json) -- every number on a card must appear in its lesson text; no duplicate fronts or near-duplicate backs."""
import html
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
lessons = {}
for L in ("L01", "L02", "L03"):
    raw = (root / f"course/modules/FC/FC1/{L}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text).replace("−", "-")
    lessons[L] = text
mine = [c for c in cards if c["lesson"] in lessons]
print("cards for L01-L03:", len(mine), "ids:", mine[0]["id"], "..", mine[-1]["id"])
bad = 0
for c in mine:
    nums = set(re.findall(r"\d[\d,]*(?:\.\d+)?", c["back"] + " " + c["front"]))
    for n in sorted(nums):
        token = n.rstrip(",")
        if token in ("1", "0") or len(token) < 2 and token not in ("1",):
            continue
        if token not in lessons[c["lesson"]] and token.replace(",", "") not in lessons[c["lesson"]]:
            print("NUMBER NOT IN LESSON:", c["id"], c["lesson"], token)
            bad += 1
print("number misses:", bad)
fr = [(c["id"], c["front"].lower()) for c in cards]
dups = [(a, b) for i, a in enumerate(fr) for b in fr[i + 1:] if SequenceMatcher(None, a[1], b[1]).ratio() > 0.8]
print("near-duplicate fronts (ratio>0.8):", dups)
bk = [(c["id"], c["back"]) for c in cards]
dupb = [(a[0], b[0], round(SequenceMatcher(None, a[1], b[1]).ratio(), 2)) for i, a in enumerate(bk) for b in bk[i + 1:] if SequenceMatcher(None, a[1], b[1]).ratio() > 0.7]
print("near-duplicate backs (ratio>0.7):", dupb)
print("duplicate ids:", len(cards) - len({c["id"] for c in cards}))
