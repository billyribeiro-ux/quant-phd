"""SC1-a round 18: dump every L01-L03 card (id, lesson, front, back, cite, grade, basis) for the full read."""

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
cards = json.load(open(os.path.join(ROOT, "course", "modules", "SC", "SC1", "cards.json"), encoding="utf-8"))
mine = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
with open(os.path.join(os.path.dirname(__file__), "out", "cards_L01_L03_r18.txt"), "w", encoding="utf-8") as out:
    for c in mine:
        out.write(f"{c['id']} {c['lesson']} | F: {c['front']} | B: {c['back']} | cite: {c['cite']} | grade: {c.get('grade')} | basis: {c.get('basis')}\n")
    out.write(f"count L01-L03 = {len(mine)}; total = {len(cards)}\n")
print("cards dumped", len(mine), "of", len(cards))
