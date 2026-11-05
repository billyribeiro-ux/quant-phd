"""Scan course/modules/LX/LX2/cards.json against the lessons for the mechanical card checks of the LX2-d slice.

Usage: python3 -I ledgers/LX2/scripts/LX2-d-r9/cards_scan.py   (run from the checkout root)
Checks: schema and counts; duplicate fronts and backs; grade values; lab read-off cards (text naming Lab 1, a
printed output, or SIMULATED) carry grade C; every numeric token of a card appears in some LX2 lesson page's visible
text (tags stripped, HTML entities decoded); every cited key is in references.json; each card id appears once.
"""

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
LX = ROOT / "course/modules/LX/LX2"
cards = json.loads((LX / "cards.json").read_text(encoding="utf-8"))
print(f"cards: {len(cards)}")
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [i for i, n in ids.items() if n > 1])
print("per lesson:", dict(Counter(c["lesson"] for c in cards)))
print("grades:", dict(Counter(c.get("grade", "-") for c in cards)))
print("keys seen:", sorted({k for c in cards for k in c}))

refs = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = {e["key"] for e in refs["entries"]}
print("unknown cite keys:", [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys])


def visible(lesson: str) -> str:
    raw = (LX / f"{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


pages = {lesson: visible(lesson) for lesson in ("L01", "L02", "L03", "L04")}
everything = " ".join(pages.values())
missing = []
for c in cards:
    body = c["front"] + " " + c["back"]
    for num in sorted(set(re.findall(r"\d[\d,]*(?:\.\d+)?", body))):
        needle = num.rstrip(",")
        if needle not in everything:
            missing.append((c["id"], num))
print("numeric tokens absent from every LX2 lesson page:", missing)

lab_pat = re.compile(r"Lab 1|printed|prints|SIMULATED|output", re.I)
print(
    "lab/printed/SIMULATED cards without grade C:",
    [c["id"] for c in cards if lab_pat.search(c["front"] + " " + c["back"] + " " + c.get("basis", "")) and c.get("grade") != "C"],
)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


fronts = Counter(norm(c["front"]) for c in cards)
backs = Counter(norm(c["back"]) for c in cards)
print("duplicate fronts:", [f[:60] for f, n in fronts.items() if n > 1])
print("duplicate backs:", [b[:60] for b, n in backs.items() if n > 1])
