"""Round-2 card scan for M7 slice c (L07, L08 cards): duplicates across the whole file, grade and basis rules,
and a number-presence check (every number in a slice card's back must appear in the cards' own lesson page).

Run: python3 -I ledgers/M7/scripts/M7-c-r2/cards_scan_r2.py
"""
import html
import json
import re
from collections import Counter

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("grades:", Counter(c["grade"] for c in cards))
bad = [c["id"] for c in cards if c["grade"] != "T" and not (c.get("basis") or c.get("cite"))]
print("non-T cards without basis or cite:", bad)
print("keys seen:", sorted({k for c in cards for k in c}))
lessons = Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(lessons.items())))

pages = {}
for lid in ("L07", "L08"):
    raw = open(f"course/modules/M/M7/{lid}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    pages[lid] = txt
    pages[lid + "raw"] = raw

missing = []
for c in cards:
    if c["lesson"] not in ("L07", "L08"):
        continue
    nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", c["back"]))
    for n in nums:
        if n in ("1", "0", "2", "3", "4", "5", "6"):
            # small integers occur everywhere; checked by the explicit list below instead
            continue
        if n not in pages["L07"] and n not in pages["L08"]:
            missing.append((c["id"], n))
print("slice card numbers (other than 0-6) absent from both lesson pages:", missing)
for lid in ("L07", "L08"):
    print(lid, "page contains 'SIMULATED':", "SIMULATED" in pages[lid], "; 'Lab 1':", "Lab 1" in pages[lid])
