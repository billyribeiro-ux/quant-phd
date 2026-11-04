"""Full scan of cards.json for duplicate ids, duplicate fronts or backs, and per-lesson card counts; slice cards listed."""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "duplicate ids:", [k for k, v in ids.items() if v > 1])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = defaultdict(list)
backs = defaultdict(list)
for c in cards:
    fronts[norm(c["front"])].append(c["id"])
    backs[norm(c["back"])].append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("duplicate backs:", [v for v in backs.values() if len(v) > 1])
slice_ids = [c["id"] for c in cards if c["lesson"] in ("L22", "L23", "L24")]
print("slice cards L22-L24:", {l: sum(1 for c in cards if c["lesson"] == l) for l in ("L22", "L23", "L24")}, "total", len(slice_ids))
# near duplicates: same first 60 normalized characters of the front
pref = defaultdict(list)
for c in cards:
    pref[norm(c["front"])[:60]].append(c["id"])
print("front-prefix collisions (60 chars):", [v for v in pref.values() if len(v) > 1])
