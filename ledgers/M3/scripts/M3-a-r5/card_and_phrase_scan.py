"""Round 5 scans for M3-a: card duplicate scan and banned/process-word grep over the slice pages.

Usage: python -I card_and_phrase_scan.py <checkout-root>
"""
import collections
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve() / "course/modules/M/M3"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
fronts = collections.Counter(" ".join(c["front"].split()).lower() for c in cards)
backs = collections.Counter(" ".join(c["back"].split()).lower() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1], "duplicate backs", [k for k, v in backs.items() if v > 1])
pats = [r"roughly", r"about \d", r"historically", r"typically", r"usually", r"can be shown", r"is easy to see",
        r"left as an exercise", r"[Bb]uilder", r"[Vv]erifier", r"\bround \d", r"[Rr]equest", r"unit report",
        r"[Aa]rchitect", r"open item"]
for f in ["index.html", "L01.html", "L02.html", "L03.html"]:
    for i, line in enumerate((root / f).read_text(encoding="utf-8").split("\n"), 1):
        for p in pats:
            if re.search(p, line):
                print(f, i, p)
                break
        if re.search(r"\.\.\.", line):
            print(f, i, "ellipsis (mathematical list only if in e1, ..., e4 form)")
