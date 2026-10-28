"""Card scans for E1 slice d, round 3: locator existence in the cited lesson, duplicate scan, grade/basis rule.

Usage: .venv/bin/python ledgers/E1/scripts/E1-d-r3/cards_scan_r3.py <checkout>
"""
import collections
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
texts = {}
for n in range(1, 10):
    raw = (root / f"L{n:02d}.html").read_text(encoding="utf-8")
    texts[f"L{n:02d}"] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
pat = re.compile(r"\b(Proposition|Lemma|Theorem|Corollary|Remark|Example|Definition|Assumption|Problem)\s+([0-9][0-9.]*|[A-Z][0-9]?)")
missing = []
for card in cards:
    for m in set(x.group(0).rstrip(".") for x in pat.finditer(card["back"] + " " + card["front"])):
        if m not in texts[card["lesson"]]:
            missing.append((card["id"], card["lesson"], m))
print("locators absent from the cited lesson:", missing)
print("ids sequential:", [c["id"] for c in cards] == [f"E1-c{i:03d}" for i in range(1, len(cards) + 1)])
print("grade counts:", collections.Counter(c.get("grade") for c in cards))
print("C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("basis without C:", [c["id"] for c in cards if c.get("basis") and c.get("grade") != "C"])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
toks = lambda s: set(re.findall(r"[a-z]+", s.lower()))
near = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        ta, tb = toks(a["front"]), toks(b["front"])
        if ta and tb and len(ta & tb) / len(ta | tb) > 0.6:
            near.append((a["id"], b["id"]))
print("near-duplicate fronts (Jaccard > 0.6):", near)
