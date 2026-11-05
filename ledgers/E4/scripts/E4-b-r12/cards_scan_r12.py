"""Round-12 E4 slice b: card scan for L04-L06 (ids, lesson attribute, duplicates, card-vs-lesson numbers)."""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE12-E4-b")
cards = json.loads((ROOT / "course/modules/E/E4/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("total cards", len(cards), "unique ids", len(set(ids)))
dup_front = [k for k, v in Counter(c["front"] for c in cards).items() if v > 1]
print("duplicate fronts:", dup_front)
dup_back = [k for k, v in Counter(c["back"] for c in cards).items() if v > 1]
print("duplicate backs:", len(dup_back))
slice_cards = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards (lesson L04-L06):", len(slice_cards))
for L in ("L04", "L05", "L06"):
    ids_L = [c["id"] for c in slice_cards if c["lesson"] == L]
    print(L, len(ids_L), ids_L[0], ids_L[-1])
# id-number monotonic check and numbers appearing in lesson text
lesson_text = {}
for L in ("L04", "L05", "L06"):
    t = (ROOT / f"course/modules/E/E4/{L}.html").read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    lesson_text[L] = re.sub(r"\s+", " ", t)
for c in slice_cards:
    nums = set(re.findall(r"\d+(?:/\d+)?", c["back"]))
    missing = [n for n in nums if n not in lesson_text[c["lesson"]]]
    if missing:
        print("NUMBER NOT IN LESSON", c["id"], missing)
print("scan done")
