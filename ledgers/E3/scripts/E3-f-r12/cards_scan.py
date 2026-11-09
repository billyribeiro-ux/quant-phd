"""Card scan (E3 slice f, round 12): ids, lesson coverage, exact and near duplicates, numbers in cards vs lesson text."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)))
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
from collections import Counter
print("slice counts", Counter(c["lesson"] for c in slice_cards), "total", len(slice_cards))
fronts = Counter(c["front"].strip().lower() for c in cards)
print("exact duplicate fronts", [f for f, n in fronts.items() if n > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("exact duplicate backs", [f[:60] for f, n in backs.items() if n > 1])


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        ta, tb = toks(a["front"]), toks(b["front"])
        jf = len(ta & tb) / max(1, len(ta | tb))
        fa, fb = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
        jfb = len(fa & fb) / max(1, len(fa | fb))
        if (jf >= 0.4 or jfb >= 0.5) and (a["lesson"] in ("L01", "L02", "L03", "L04") or b["lesson"] in ("L01", "L02", "L03", "L04")):
            pairs.append((round(jf, 2), round(jfb, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)

# numbers in card front/back must appear in the lesson html of the same lesson
bad = []
for c in slice_cards:
    html = (ROOT / f"course/modules/E/E3/{c['lesson']}.html").read_text(encoding="utf-8")
    for num in set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"])):
        if num not in html:
            bad.append((c["id"], num))
print("numbers absent from lesson html:", bad)
