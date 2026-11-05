"""Round-11 cards scan for E4 L04-L06: duplicate ids, near-duplicate fronts/backs, card-to-lesson numeric presence."""

from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
cards = json.loads((ROOT / "course/modules/E/E4/cards.json").read_text(encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards", len(sl), "ids unique", len({c["id"] for c in sl}) == len(sl))
tok = lambda s: set(re.findall(r"[A-Za-zα-ωΑ-Ω0-9_]+", s.lower()))  # noqa: E731
pairs = []
for a, b in combinations(sl, 2):
    fa, fb = tok(a["front"]), tok(b["front"])
    ba, bb = tok(a["back"]), tok(b["back"])
    jf = len(fa & fb) / max(1, len(fa | fb))
    jb = len(ba & bb) / max(1, len(ba | bb))
    if jf >= 0.6 or (jf >= 0.4 and jb >= 0.6):
        pairs.append((round(jf, 2), round(jb, 2), a["id"], b["id"]))
print("near-duplicate pairs (front Jaccard>=0.6, or front>=0.4 and back>=0.6):", len(pairs))
for p in sorted(pairs, reverse=True):
    print(p)
# cards with grade T must carry basis; cards with cite must have registry key
reg = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = set()
if isinstance(reg, dict):
    keys = set(reg.get("entries", reg).keys()) if isinstance(reg.get("entries", reg), dict) else set()
elif isinstance(reg, list):
    keys = {r.get("key") for r in reg}
print("registry keys loaded", len(keys), "muth1961rational present", "muth1961rational" in keys)
for c in sl:
    if c.get("grade") in ("T", "A", "B", "C") and "basis" not in c and not c.get("cite"):
        print("NO BASIS", c["id"])
    for k in c.get("cite", []):
        print("cite", c["id"], k, k in keys)
