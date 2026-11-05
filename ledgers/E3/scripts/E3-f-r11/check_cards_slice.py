"""E3 slice f round 11: card integrity, numbers-in-lesson, token-Jaccard duplicate scan for L01-L04 cards.

Run from the checkout root: python3 -I ledgers/E3/scripts/E3-f-r11/check_cards_slice.py
"""
import itertools
import json
import re
from pathlib import Path

ROOT = Path(".")
UNIT_DIR = ROOT / "course/modules/E/E3"
cards = json.loads((UNIT_DIR / "cards.json").read_text(encoding="utf-8"))
lessons = {f"L0{i}": (UNIT_DIR / f"L0{i}.html").read_text(encoding="utf-8") for i in range(1, 9)}
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)))
per = {}
for c in cards:
    per[c["lesson"]] = per.get(c["lesson"], 0) + 1
print("per lesson", dict(sorted(per.items())))
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice cards", len(slice_cards))

NUM = re.compile(r"(?<![A-Za-z_])(\d+(?:\.\d+)?)(?![\d])")
print("--- numbers in card text that do not occur in the card's lesson HTML (as substrings) ---")
for c in slice_cards:
    text = c["front"] + " " + c["back"]
    html = lessons[c["lesson"]]
    for n in sorted(set(NUM.findall(text))):
        if n in ("0", "1", "2", "3", "4", "5", "6", "10"):
            continue
        if n not in html:
            print(c["id"], c["lesson"], "number", n, "not in lesson HTML")

print("--- token Jaccard >= 0.4 on front+back across all 178 cards (pairs involving a slice card) ---")
def toks(s):
    return set(re.findall(r"[a-z]+", s.lower())) - {"the", "a", "of", "and", "is", "in", "to", "for", "under", "what", "does", "on", "with", "at", "that", "it", "this", "by", "as", "an", "or", "be", "from"}
sl = {c["id"] for c in slice_cards}
for a, b in itertools.combinations(cards, 2):
    if a["id"] not in sl and b["id"] not in sl:
        continue
    ta, tb = toks(a["front"]), toks(b["front"])
    fj = len(ta & tb) / max(1, len(ta | tb))
    ta2, tb2 = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
    j = len(ta2 & tb2) / max(1, len(ta2 | tb2))
    if fj >= 0.4 or j >= 0.5:
        print(a["id"], b["id"], "front_jaccard", round(fj, 2), "full_jaccard", round(j, 2))
print("--- grades / basis rule: grade != T needs cite or basis ---")
for c in cards:
    if c.get("grade") not in (None, "T") and not (c.get("cite") or str(c.get("basis", "")).strip()):
        print("PROBLEM", c["id"])
print("done")
