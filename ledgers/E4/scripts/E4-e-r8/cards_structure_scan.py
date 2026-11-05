"""Round 8, slice e: structure, duplicate, grade, banned-phrase and near-duplicate scan of cards.json (E4).

Usage: python -I cards_structure_scan.py <cards.json>
"""
import collections
import difflib
import itertools
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("cards", len(cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)), "duplicate ids", [i for i, n in collections.Counter(ids).items() if n > 1])
print("duplicate fronts", [f[:60] for f, n in collections.Counter(c["front"] for c in cards).items() if n > 1])
print("duplicate backs", [b[:60] for b, n in collections.Counter(c["back"] for c in cards).items() if n > 1])
nums = sorted(int(i.split("-c")[-1]) for i in ids)
print("id numbers c001..c%03d not assigned" % max(nums), [n for n in range(1, max(nums) + 1) if n not in nums])
print("lessons", sorted(collections.Counter(c["lesson"] for c in cards).items()))
print("key sets", collections.Counter(tuple(sorted(c.keys())) for c in cards))
print("grades", collections.Counter(c.get("grade") for c in cards))
print("C cards", [c["id"] for c in cards if c.get("grade") == "C"])
print("cards without basis but with grade", [c["id"] for c in cards if c.get("grade") and not c.get("basis")])
print("cards with cite", [(c["id"], c["cite"]) for c in cards if c.get("cite")])
pats = [r"TODO", r"TBD", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
        r"left as an exercise", r"you can add", r"it is important to note", r"studies show", r"experts agree",
        r"well known", r"[Oo]bviously", r"[Cc]learly", r"\bbatch\b", r"\bround\b", r"\bverifier\b", r"\bbuilder\b",
        r"fixed in", r"\bupdated\b", r"\brevised\b", r"\bprevious\b", r"[Ii]t can be shown", r"we changed"]
hits = []
for c in cards:
    body = c["front"] + " || " + c["back"] + " || " + (c.get("basis") or "")
    for p in pats:
        if re.search(p, body):
            hits.append((c["id"], p))
print("banned or process-word hits", hits)
print("fronts not ending in ? . )", [c["id"] for c in cards if not c["front"].strip().endswith(("?", ".", ")"))])
pairs = []
for a, b in itertools.combinations(cards, 2):
    r1 = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
    r2 = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
    if r1 > 0.75 or r2 > 0.85:
        pairs.append((round(r1, 2), round(r2, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.75 or back>0.85):", len(pairs))
for p in sorted(pairs, reverse=True):
    print("  ", p)
