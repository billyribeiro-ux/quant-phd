"""Round 10, slice E4-c: structural scan of course/modules/E/E4/cards.json (duplicates, per-lesson counts, L07-L09 ids)."""
import collections
import json
import re
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/wt/verifyE10-E4-c")
cards = json.loads((BASE / "course/modules/E/E4/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards))
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
print("duplicate fronts (normalised)", [k[:60] for k, v in collections.Counter(norm(c["front"]) for c in cards).items() if v > 1])
print("duplicate backs (normalised)", [k[:60] for k, v in collections.Counter(norm(c["back"]) for c in cards).items() if v > 1])
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
for lesson in ("L07", "L08", "L09"):
    sel = [c["id"] for c in cards if c["lesson"] == lesson]
    print(lesson, len(sel), sel[0], "...", sel[-1], "ids:", " ".join(i.split("-")[1] for i in sel))
print("missing card numbers in E4-c130..E4-c250 range:", [n for n in range(130, 251) if f"E4-c{n}" not in ids])
print("grades:", collections.Counter(c.get("grade") for c in cards))
