"""Round-11 M3 slice c: full scan of cards.json for duplicate ids, duplicate or near-duplicate fronts/backs,
grade/basis rules (BUILDER_RULES 7), and lesson/grade field validity."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD11-M3-c")
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("id sequence gaps:", sorted(set(f"M3-c{n:03d}" for n in range(1, 214)) - set(ids)))
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
fronts = {}
backs = {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
    backs.setdefault(norm(c["back"]), []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])
tok = lambda s: set(norm(s).split())
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = tok(cards[i]["front"]), tok(cards[j]["front"])
        if not a or not b:
            continue
        jac = len(a & b) / len(a | b)
        if jac >= 0.6:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"], cards[i]["front"][:70], cards[j]["front"][:70]))
print("front Jaccard >= 0.6 pairs:", len(pairs))
for p in sorted(pairs, reverse=True)[:20]:
    print("  ", p)
allowed_grades = {"T", "A", "B", "C", "D", "X", None}
bad = []
for c in cards:
    if c.get("grade") not in allowed_grades:
        bad.append((c["id"], "grade", c.get("grade")))
    if c.get("grade") == "C" and not c.get("basis"):
        bad.append((c["id"], "C without basis"))
    if c["lesson"] not in {f"L{n:02d}" for n in range(1, 10)}:
        bad.append((c["id"], "lesson", c["lesson"]))
print("rule violations:", bad)
