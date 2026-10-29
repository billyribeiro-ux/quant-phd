"""Round-7 scan of course/modules/E/E2/cards.json: structure, duplicates, numbers-in-lesson, changed cards."""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E2 = ROOT / "course/modules/E/E2"
cards = json.loads((E2 / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", [k for k, v in collections.Counter(ids).items() if v > 1])
print("id sequence gaps:", sorted(set(f"E2-c{n:03d}" for n in range(1, len(cards) + 1)) - set(ids)))
fronts = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(re.sub(r"\W+", " ", c["back"].lower()).strip() for c in cards)
print("duplicate backs:", [k[:80] for k, v in backs.items() if v > 1])
print("keys:", sorted({tuple(sorted(c)) for c in cards}))
print("grades:", collections.Counter(c.get("grade") for c in cards))
print("lessons:", collections.Counter(c["lesson"] for c in cards))
lessons = {L: (E2 / f"{L}.html").read_text(encoding="utf-8") for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"]}
allp = "\n".join(lessons.values())
for c in cards:
    nums = re.findall(r"\d[\d,]*(?:\.\d+)?", c["front"] + " " + c["back"])
    text = lessons[c["lesson"]]
    for n in nums:
        m = n.rstrip(".,")
        if m.replace(",", "") in ("1", "2", "0", "3", "4", "5"):
            continue
        if m not in text and m.replace(",", "") not in text.replace(",", ""):
            print("number not in own lesson:", c["id"], c["lesson"], repr(m), "| in project:", m in allp)
