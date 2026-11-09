"""FC1-b round 5: full-file card scan. Duplicate ids and fronts, near-duplicate fronts or backs (token Jaccard), and
every parenthesised locator in a card's back checked against the lessons' text for the lesson the card names."""

import itertools
import json
import re
from pathlib import Path

ROOT = Path(".").resolve()
cards = json.loads((ROOT / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
pages = {p: (ROOT / f"course/modules/FC/FC1/{p}.html").read_text(encoding="utf-8") for p in ["L01", "L02", "L03", "L04", "L05"]}


def toks(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


print("cards", len(cards))
print("dup ids", len({c["id"] for c in cards}) != len(cards))
print("dup fronts", len({c["front"].strip().lower() for c in cards}) != len(cards))
close = []
for a, b in itertools.combinations(cards, 2):
    fa, fb = toks(a["front"]), toks(b["front"])
    ba, bb = toks(a["back"]), toks(b["back"])
    jf = len(fa & fb) / max(1, len(fa | fb))
    jb = len(ba & bb) / max(1, len(ba | bb))
    if jf > 0.5 or jb > 0.6:
        close.append((round(jf, 2), round(jb, 2), a["id"], b["id"]))
print("near-duplicate pairs (front J>0.5 or back J>0.6):")
for row in close:
    print("  ", row)
print("== locator check: each card back's 'Definition/Remark/Proposition/Example/Problem/Assumption/Section/misconception N' must appear in its lesson")
pat = re.compile(r"(Definition \d\.\d|Remark \d\.\d|Proposition \d\.\d|Example \d\.\d|Problem [A-Z]\d|Assumption A\d|Section \d|misconception \d)")
missing = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = pages[c["lesson"]]
    for loc in pat.findall(c["back"] + " " + c["front"]):
        probe = loc
        if probe.startswith("misconception"):
            if not re.search(r"misconception|Misconception", text):
                missing.append((c["id"], loc))
            continue
        if probe.startswith("Section"):
            n = probe.split()[1]
            if not re.search(rf'<span class="section-number">{n}</span>', text):
                missing.append((c["id"], loc))
            continue
        if probe.startswith("Assumption"):
            if probe not in text:
                missing.append((c["id"], loc))
            continue
        if probe not in text and probe.replace(" ", " ") not in text:
            missing.append((c["id"], loc))
print("card locators not found in own lesson:", missing)
